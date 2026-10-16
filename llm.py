import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY")

classify_llm = ChatOpenAI(
    api_key = api_key ,
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0
)