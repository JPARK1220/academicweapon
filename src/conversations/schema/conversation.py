from mongoengine import Document, ObjectIdField, StringField, DateTimeField, DictField, ListField, EmbeddedDocumentField
from datetime import datetime, timezone

from conversations.constants import STANDARD_CHARS_REGEX
from src.llm.utils import models

class Conversation(Document):
    user_id = ObjectIdField(required=True)
    title = StringField(
        required=True, min_length=4, max_length=32, regex=STANDARD_CHARS_REGEX
    )
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    status = StringField(
        required=True, choices=["active", "archived", "deleted"], default="active"
    )
    metadata = DictField()

    # Add tokens used etc

    # Array of messages (schema) here

    # Add other parameters for settings, like temperature etc (see open router reference), additionally you can set max tokens
    settings = DictField(
        default={
            "model": models.default,
        }
    )

    meta = {  # Add compound indexes that are needed
        "collection": "conversations",  # Name of collection
        "indexes": [
            "user_id",
            "status",
            ("user_id", "status"),
            ("user_id", "-created_at"),
        ],
    }

    def clean(self):
        self.updated_at = datetime.now(timezone.utc)
