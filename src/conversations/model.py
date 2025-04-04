from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
import re

from src.conversations.constants import CONVERSATION_ROLES, STANDARD_CHARS_REGEX
from src.llm.utils import Topic, models

# Constants
TITLE_REGEX = re.compile(STANDARD_CHARS_REGEX)

class CreateMessageRequest(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

    # Add a limit of 1 in future
    image_urls: Optional[List[str]] = Field(default=[], description="List of image URLs attached to the message") 
    
    @field_validator('role')
    def validate_role(cls, value):
        if value != "user":
            raise ValueError('Role must be one of: user, assistant, system')
        return value
    
    @model_validator(mode='after')
    def validate_content_or_images(self):
        if not (self.content or len(self.image_urls)):
            raise ValueError("Either content must be provided or image_urls must have at least one URL")
        return self

class CreateSettingsRequest(BaseModel):
    # model, temperature, max_tokens - We probably won't use these parameters here as we want to abstract it away from the frontend.
    topic: Topic = Field(default=Topic.DEFAULT, description="topic of the conversation")

class CreateConversationRequest(BaseModel):
    title: str = Field(..., min_length=4, max_length=32, description="Title of the conversation")
    settings: Optional[CreateSettingsRequest] = Field(default_factory=CreateSettingsRequest, description="Conversation settings")
    # metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata") <- Maybe define by backend instead
    message: CreateMessageRequest = Field(..., description="Initial message in the conversation")

    @field_validator('title')
    def validate_title(cls, value):
        if not TITLE_REGEX.match(value):
            raise ValueError("Title contains invalid characters")
        return value