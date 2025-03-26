from mongoengine import Document, ObjectIdField, StringField, DateTimeField, DictField
from datetime import datetime, timezone

from conversations.constants import STANDARD_CHARS_REGEX
from src.llm.utils import models

class Conversation(Document):
  user_id = ObjectIdField(required=True)
  title = StringField(required=True, min_length=4, max_length=32, regex=STANDARD_CHARS_REGEX)
  created_at = DateTimeField(default=datetime.now(timezone.utc))
  updated_at = DateTimeField(default=datetime.now(timezone.utc))
  status = StringField(required=True, choices=['active', 'archived', 'deleted'], default='active')
  metadata = DictField()

  # Add other parameters
  settings = DictField(default={
    'model': models.default,
  })

  meta = {
    'collection': 'conversations',
    'indexes': [
      'user_id',
      'status',
    ]
  }

  def clean(self):
    self.updated_at = datetime.now(timezone.utc)

  