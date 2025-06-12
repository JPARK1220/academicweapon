from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    # Primary Keys
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), primary_key=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), primary_key=True)

    order_index = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="conversation_messages")
    message = relationship("Message", back_populates="conversation_messages")