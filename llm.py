import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY")
ttq_api_key = os.getenv("TTQ_API_KEY")

classify_llm = ChatOpenAI(
    api_key = api_key ,
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0.5
)

ttq_llm = ChatOpenAI(
    api_key = ttq_api_key,
    base_url="https://openrouter.ai/api/v1",
    model="cohere/north-mini-code:free",
    temperature=0.5
)

relevance_llm = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)