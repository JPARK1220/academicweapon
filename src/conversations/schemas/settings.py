from pydantic import BaseModel, Field

class Settings(BaseModel):
    topic: str = Field()