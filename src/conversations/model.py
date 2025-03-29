from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re

from src.conversations.constants import CONVERSATION_ROLES, STANDARD_CHARS_REGEX
from src.llm.utils import models

# Constants
TITLE_REGEX = re.compile(STANDARD_CHARS_REGEX)

class MessagesRequest(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

    # Add a limit of 1 in future
    image_urls: Optional[List[str]] = Field(default=[], description="List of image URLs attached to the message") 
    
    @field_validator('role')
    def validate_role(cls, value):
        if value not in CONVERSATION_ROLES:
            raise ValueError('Role must be one of: user, assistant, system')
        return value

class SettingsRequest(BaseModel):
    model: Optional[str] = Field(default=models['default'], description="LLM model to use")
    # temperature: Optional[float] = Field(default=0.7, ge=0, le=1, description="Temperature for model generation")
    # max_tokens: Optional[int] = Field(default=1000, gt=0, description="Maximum number of tokens for response") <- Defined by backend and user data
    
    @field_validator('model', mode='after')
    def validate_model(cls, value):
        if value not in models:
            raise ValueError(f"Invalid model specification")
        return value

class CreateConversationRequest(BaseModel):
    title: str = Field(..., min_length=4, max_length=32, description="Title of the conversation")
    settings: Optional[SettingsRequest] = Field(default_factory=SettingsRequest, description="Conversation settings")
    # metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata") <- Maybe define by backend instead
    message: MessagesRequest = Field(..., description="Initial message in the conversation")

    @field_validator('title')
    def validate_title(cls, value):
        if not TITLE_REGEX.match(value):
            raise ValueError("Title contains invalid characters")
        return value

# class UpdateConversationSettingsRequest(BaseModel):
#     model: Optional[str] = None
#     temperature: Optional[float] = Field(None, ge=0, le=1)
#     max_tokens: Optional[int] = Field(None, gt=0)
    
#     @model_validator
#     def check_at_least_one_field(cls, values):
#         if not any(values.values()):
#             raise ValueError("At least one setting must be provided")
#         return values
    
#     @field_validator('model')
#     def validate_model(cls, value):
#         if value is not None and value not in models.available_models:
#             raise ValueError(f"Model must be one of: {', '.join(models.available_models)}")
#         return value

# class UpdateConversationStatusRequest(BaseModel):
    # status: str = Field(..., description="New status for the conversation")
    
    # @field_validator('status')
    # def validate_status(cls, value):
    #     if value not in ['active', 'archived', 'deleted']:
    #         raise ValueError("Status must be one of: active, archived, deleted")
    #     return value