import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from src.conversations.constants import ConversationRoles

class Message(BaseModel):
    message_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role: ConversationRoles 
    content: Optional[str] = None
    image_urls: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
