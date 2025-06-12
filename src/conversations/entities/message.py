from src.database import Base
from sqlalchemy import Column, String, DateTime, Text, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from datetime import datetime, timezone

class Message(Base):
    __tablename__ = "messages"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conversation_messages = relationship("ConversationMessage", back_populates="message")
