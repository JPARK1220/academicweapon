
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.database import Base

import uuid
from datetime import datetime, timezone

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(String, nullable=False, index=True)

    title = Column(String(32), nullable=False)
    status = Column(String(20), default="active")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    settings = Column(JSONB, default=dict, nullable=False)

    conversation_messages = relationship("ConversationMessage", back_populates="conversation", order_by="ConversationMessage.order_index")