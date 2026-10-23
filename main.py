from pydantic import BaseModel
from ttq import text_to_query
from qtr import query_to_result
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi import UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from pathlib import Path

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

uploaded_dataset_path =None

from generation.data import create_vb
from memory import init_memory, save_interaction, get_last_k_message

create_vb()
init_memory()


app = FastAPI()

transcript = []

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Text-to-SQL API is running"}

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    global uploaded_dataset_path, uploaded_dataset_columns

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file"
        )

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        df = pd.read_csv(BytesIO(content))

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The dataset contains no rows"
            )

        file_path = UPLOAD_DIR / Path(file.filename).name
        file_path.write_bytes(content)

        uploaded_dataset_path = file_path
        uploaded_dataset_columns = df.columns.tolist()

        return {
            "message": "Dataset uploaded successfully",
            "filename": file_path.name,
            "rows": len(df),
            "columns": uploaded_dataset_columns,
            "data": df.head(5).to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read CSV: {str(e)}"
        )
    finally:
        await file.close()

@app.post("/execute")
def execute_query(request: TextRequest):
    text = request.text.strip()
    
    if not text:
        return {"message": "Empty text ignored"}

    transcript.append(text)

    if uploaded_dataset_path is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first"
        )

    full_text = " ".join(transcript)

    try:
        memory = get_last_k_message(5)
        sql_query = text_to_query(
            full_text,
            file_name=uploaded_dataset_path.name,
            columns=uploaded_dataset_columns,
            memory=memory
        )
        result = query_to_result(sql_query)

        save_interaction(
            user_message=request.text,
            intent="none",
            assistant_response=sql_query,
        )

        return {
            "question": full_text,
            "sql_query": sql_query,
            "result": result
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


