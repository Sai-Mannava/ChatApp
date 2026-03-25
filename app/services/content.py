import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import ContentType, WritingEntry, WritingSession


class SessionNotFoundError(ValueError):
    pass


class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self) -> WritingSession:
        session = WritingSession(id=str(uuid.uuid4()))
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: str) -> WritingSession:
        stmt = (
            select(WritingSession)
            .where(WritingSession.id == session_id)
            .options(selectinload(WritingSession.entries))
        )
        session = self.db.scalar(stmt)
        if session is None:
            raise SessionNotFoundError(f"Session {session_id} not found")
        session.entries.sort(key=lambda item: item.created_at)
        return session

    def add_entry(
        self,
        session_id: str,
        content_type: ContentType,
        input_text: str,
        output_text: str,
    ) -> WritingEntry:
        _ = self.get_session(session_id)

        entry = WritingEntry(
            id=str(uuid.uuid4()),
            session_id=session_id,
            content_type=content_type,
            input_text=input_text,
            output_text=output_text,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry
