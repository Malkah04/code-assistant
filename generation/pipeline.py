from generation.eval import check_relevance
from llm import classify_llm

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from generation.feedback import save_user_solution


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="ai_assistant",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


prompt = ChatPromptTemplate.from_template("""
You are a code generation assistant.

User request:
{question}

Relevant programming examples:
{context}

Instructions:
- Generate complete, runnable source code.
- Follow the programming language requested by the user.
- Use meaningful variable and function names.
- Follow language-specific best practices.
- Add comments where they clarify non-obvious logic.
- Include appropriate error handling when necessary.
- Consider edge cases.
- Use the retrieved examples as supporting knowledge,
  not as code to copy blindly.
- If essential requirements are ambiguous, ask for clarification.
- Return the code inside a Markdown code block with
  the appropriate language identifier.
- Do not claim that the code was tested unless it actually was.
Previous conversation:
{memory}

""")


generation_chain = prompt | classify_llm


def generate_code(question ,memory=""):
    if not question.strip():
        return "Please enter a programming request."

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    for doc in docs:
        print("Task ID:", doc.metadata.get("task_id"))
        print("Entry Point:", doc.metadata.get("entry_point"))
        print("Content:", doc.page_content[:300])
        print("-" * 40)


    if not docs:
        return (
            "I couldn't find relevant knowledge for your request. "
            "Could you provide the correct solution or reference "
            "so I can learn from it?"
        )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Step 3: Evaluate relevance
    relevant = check_relevance(
        question=question,
        context=context
    )

    if not relevant:
        return (
            "I couldn't find relevant knowledge for your request. "
            "Could you provide the correct solution or reference "
            "so I can learn from it?"
        )

    response = generation_chain.invoke({
        "question": question,
        "context": context,
        "memory":memory
    })

    return response.content.strip()


#