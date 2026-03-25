from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ContentType(str, Enum):
    GENERATED = "generated"
    EDITED = "edited"
    REFINED = "refined"


class WritingSession(Base):
    __tablename__ = "writing_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    entries: Mapped[list["WritingEntry"]] = relationship(
        "WritingEntry", back_populates="session", cascade="all, delete-orphan"
    )


class WritingEntry(Base):
    __tablename__ = "writing_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("writing_sessions.id"), index=True)
    content_type: Mapped[ContentType] = mapped_column(SqlEnum(ContentType), nullable=False)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    session: Mapped[WritingSession] = relationship("WritingSession", back_populates="entries")
