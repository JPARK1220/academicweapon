from pydantic import BaseModel

class ImageRequest(BaseModel):
    topic: str
    image_urls: list[str]
    
class ImageResponse(BaseModel):
    result: str
