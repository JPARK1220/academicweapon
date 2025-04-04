from typing import List
from fastapi import HTTPException
from .models import LlmRequest, LlmResponse
from .utils import Topic, get_model
from openai import AsyncOpenAI

# Todo: get_llm_response should be a service

class LlmService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def process(self, request: LlmRequest):
        try:
            result = await self.get_llm_response(request.topic, request.image_urls)
            return LlmResponse(result=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_llm_response(self, topic: Topic, conversation: List):
        response = await self.client.chat.completions.create(
            model=get_model(topic),
            messages=conversation,
            max_completion_tokens=1000,
        )
        return response.choices[0].message.content
    
    # Make schema