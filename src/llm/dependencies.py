from .service import LlmService
from openai import AsyncOpenAI
from dotenv import load_dotenv
from functools import lru_cache
import os

@lru_cache()
def get_openai_client():
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

def get_llm_service():
    client = get_openai_client()
    return LlmService(client=client)