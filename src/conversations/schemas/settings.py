from pydantic import BaseModel, Field
from src.llm.utils import models

class Settings(BaseModel):
    model: str = Field(default=models["default"])