from pydantic import BaseModel


class LlmRequest(BaseModel):
    model: str
    image_urls: list[str]


class LlmResponse(BaseModel):
    result: str
