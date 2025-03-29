from beanie import Document
from pydantic import Field
from typing import List, Optional, Literal
from datetime import datetime, timezone

from ..constants import STANDARD_CHARS_REGEX
from .message import Message
from .settings import Settings

class Conversation(Document):
    user_id: str
    title: str = Field(..., min_length=4, max_length=32, pattern=STANDARD_CHARS_REGEX)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: Literal["active", "archived", "deleted"] = Field(default="active")
    metadata: Optional[dict] = Field(default_factory=dict)

    messages: List[Message] = Field(default_factory=list)
    settings: Settings

    class Settings: 
        name = "conversations"  # collection name
        indexes = [
            "user_id",
            "status",
            [("user_id", 1), ("status", 1)],
            [("user_id", 1), ("created_at", -1)],
        ]

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
