import uuid
from datetime import datetime, timezone
from mongoengine import EmbeddedDocument, UUIDField, StringField, ListField, DateTimeField

class Message(EmbeddedDocument):
    message_id = UUIDField(binary=False, default=uuid.uuid4, required=True)
    role = StringField(required=True, choices=['user', 'assistant', 'system'])
    content = StringField()
    image_urls = ListField(StringField())
    timestamp = DateTimeField(default=datetime.now(timezone.utc))