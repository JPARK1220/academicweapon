from typing import List, Dict
from fastapi import HTTPException
from .models import LlmRequest, LlmResponse
from .utils import Model
from openai import AsyncOpenAI

class LlmService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def process(self, request: LlmRequest):
        try:
            result = await self.generate_llm_response(request.model, request.image_urls)
            return LlmResponse(result=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_llm_response(self, model: str, conversation: List[Dict]):
        response = await self.client.chat.completions.create(
            model=model,
            messages=conversation,
            max_completion_tokens=1000,
        )
        return response.choices[0].message.content
    
    # Make schema