from langchain_core.prompts import PromptTemplate
from llm import classify_llm


prompt =PromptTemplate.from_template(
    """
    You are an intent classifier for an AI Coding Assistant.
    Classify the user's request into exactly one category:

    EXPLAIN:
    The user wants to understand, debug, analyze, or explain
    existing code or an existing programming error.

    GENERATE:
    The user wants to create new code, implement a feature,
    build an application, or write a new function.

    Return exactly one label: EXPLAIN or GENERATE.
    Do not add any other text.
    
    User request:
    {query}

"""
)
query =""
chain = prompt | classify_llm


def classify(query: str) -> str:
    if not query.strip():
        raise ValueError("The query cannot be empty.")

    response = chain.invoke({"query": query})

    return response.content.strip()

# res= classify("Write a function that checks whether any two numbers in a list are closer than a given threshold.")
# print(res)