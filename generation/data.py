import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

df =pd.read_csv("openai_humaneval.csv")
# print(list(df.head()))
# print(df.iloc[10].to_dict())
# print(len(df))

required_columns = [
    "task_id",
    "prompt",
    "canonical_solution",
    "test",
    "entry_point",
]


assert all(col in df.columns for col in required_columns)

df = df.drop_duplicates(subset=["task_id"])

df = df.dropna(
    subset=["task_id", "prompt", "canonical_solution", "entry_point" ,"test"]
)

documents =[]

for _ ,row in df.iterrows():
    content =(
        f"programming task :\n{row["prompt"]}\n\n"
        f"reference solution :\n {row["canonical_solution"]}\n\n"
        f"test cases:\n{row['test']}"
    )
    metadata ={
        "task_id":str(row["task_id"]),
        "entry_point":str(row["entry_point"]),
        "source": "openai_humaneval.csv",
    }
    document = Document(
        page_content=content,
        metadata=metadata,
    )
    documents.append(document)

# print("Number of documents:", len(documents))
# print("\nFirst document:")
# print(documents[0].page_content)
# print("\nMetadata:")
# print(documents[0].metadata)


# embedding_model =HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )
# vector_store = Chroma.from_documents(
#     documents=documents,
#     embedding=embedding_model,
#     collection_name="ai_assistant",
#     persist_directory="./chroma_db"
# )

# print("Number of stored documents:", vector_store._collection.count())


query = """
Write a Python function that checks whether
any two numbers in a list are closer than a
given threshold.
"""

# results = vector_store.similarity_search(
#     query,
#     k=3
# )

# for i, doc in enumerate(results, start=1):
#     print(f"\n--- Result {i} ---")
#     print("Task ID:", doc.metadata["task_id"])
#     print("Entry Point:", doc.metadata["entry_point"])
#     print("Content:\n", doc.page_content)



def create_vb():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name="ai_assistant",
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )

    if vector_store._collection.count() == 0:
        vector_store.add_documents(
            documents=documents,
            ids=[doc.metadata["task_id"] for doc in documents]
        )

        print("Knowledge base created.")

    else:
        print("Knowledge base already contains documents.")

    return vector_store
