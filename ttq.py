from langchain_core.prompts import ChatPromptTemplate
from llm import ttq_llm ,classify_llm ,relevance_llm


prompt ="""
You are a programming assistant that converts natural language programming requests into structured SQL queries.
and this is my table name {file_name} , and this is my table columns {columns}.
Previous conversation:
{memory}

User request:
{text}
Instructions:
- Generate a SQL query that accurately represents the user's request.
- Ensure the query is syntactically correct and follows best practices.
- If the request is ambiguous, make reasonable assumptions and document them in comments.
- Return only the SQL query without any additional explanations or text.
"""

prompt = ChatPromptTemplate.from_template(prompt)
chain = prompt | ttq_llm
    

def text_to_query(text ,file_name, columns, memory=""):
    query = chain.invoke({"text": text, "file_name": file_name, "columns": columns, "memory": memory})
    return query

# query =text_to_query("i want to know whose salary is greater than 50000 in the employees table")
# print(query.content)