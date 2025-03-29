from mongoengine import EmbeddedDocument, StringField
from src.llm.utils import models

class Settings(EmbeddedDocument):
    model = StringField(default=models.default)

    # in the future, we can add temperature, max tokens, etc.