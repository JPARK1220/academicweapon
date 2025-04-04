from pydantic import BaseModel


class LlmRequest(BaseModel):
    topic: str
    image_urls: list[str]


class LlmResponse(BaseModel):
    result: str
