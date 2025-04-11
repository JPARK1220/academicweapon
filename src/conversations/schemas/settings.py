from pydantic import BaseModel, Field

# Change to use Topic enum
class Settings(BaseModel):
    topic: str = Field()