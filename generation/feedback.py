from uuid import uuid4

from langchain_core.documents import Document
from generation.data import create_vb


def save_user_solution(question: str, solution: str) -> str:
    question = question.strip()
    solution = solution.strip()

    if not question or not solution:
        raise ValueError("Question and solution cannot be empty.")

    vector_store = create_vb()
    feedback_id = str(uuid4())

    document = Document(
        page_content=(
            f"Programming task:\n{question}\n\n"
            f"Reference solution:\n{solution}"
        ),
        metadata={
            "source": "user_feedback",
            "type": "user_solution",
            "feedback_id": feedback_id,
        },
    )

    vector_store.add_documents(
        documents=[document],
        ids=[feedback_id],
    )

    saved = vector_store.get(
        ids=[feedback_id],
        include=["documents", "metadatas"],
    )

    if not saved["ids"]:
        raise RuntimeError("The solution was not found after saving.")

    print("Reference solution saved successfully.")
    print("Feedback ID:", feedback_id)
    print("Saved metadata:", saved["metadatas"][0])

    return "Reference solution saved and verified successfully."
