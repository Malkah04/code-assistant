from langchain_core.prompts import ChatPromptTemplate
from llm import classify_llm


prompt = """
You are an expert programming tutor.

Your task is to explain existing code and programming errors.

Instructions:
- Explain the code clearly and accurately.
- Explain the logic step by step when appropriate.
- If the user provides an error, explain its likely cause.
- If code is provided, refer to the relevant parts.
- Do not invent code or output that cannot be inferred.
- If the user did not provide the code needed for an
  accurate explanation, ask them to provide it.
- Use the conversation history when the user refers
  to previous questions, code, or explanations.
- Do not assume the current request refers to previous
  code unless the context supports that interpretation.

Previous conversation:
{memory}

Current user request:
{query}
"""

prompt = ChatPromptTemplate.from_template(prompt)

chain = prompt | classify_llm

def explain_code(query , memory=""):
    if not query.strip():
        raise ValueError("The query cannot be empty.")

    response = chain.invoke({"query": query ,"memory": memory})

    return response.content

