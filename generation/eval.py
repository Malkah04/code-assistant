from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

relevance_llm = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a relevance evaluator for a programming assistant.

Determine whether the retrieved context contains enough
relevant information to help answer the user's request.

User request:
{question}

Retrieved context:
{context}

Reply with exactly one word:
Relevant
or
Not Relevant
""")

chain = prompt | relevance_llm


def check_relevance(question , context):
    if not question.strip() or not context.strip():
        return False
    
    response = chain.invoke({
        "question": question,
        "context": context
    })

    result = response.content.strip().lower().rstrip(".!,:;")

    if result == "relevant":
        return True

    if result == "not relevant":
        return False
    
    print("Unexpected relevance response:", repr(response.content))
    return False


question = "Write code to remove duplicate rows using Pandas."

context = """
Pandas DataFrames can remove duplicate rows
using the drop_duplicates() method.
"""

# print(check_relevance(question, context))
