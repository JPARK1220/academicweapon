from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from datetime import datetime, timezone


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    filename = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=False)
    mime_type = Column(String(255), nullable=False)
    file_size = Column(Integer)

    bucket_name = Column(String(255), nullable=False)
    object_key = Column(String(255), nullable=False)