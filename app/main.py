import time
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import ContentType
from app.schemas import (
    SessionCreateResponse,
    SessionDetailResponse,
    WriteEditRequest,
    WriteGenerateRequest,
    WriteRefineRequest,
    WriteResponse,
)
from app.services.ai import AIWriterService
from app.services.content import ContentService, SessionNotFoundError


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Writing Assistant", version="1.0.0", lifespan=lifespan)
ai_writer = AIWriterService()


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-MS"] = str(elapsed_ms)
    return response


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except SQLAlchemyError:
        return {"status": "degraded", "database": "error"}


@app.post("/api/sessions", response_model=SessionCreateResponse)
def create_session(db: Session = Depends(get_db)) -> SessionCreateResponse:
    session = ContentService(db).create_session()
    return SessionCreateResponse(session_id=session.id)


@app.get("/api/sessions/{session_id}", response_model=SessionDetailResponse)
def get_session(session_id: str, db: Session = Depends(get_db)) -> SessionDetailResponse:
    try:
        session = ContentService(db).get_session(session_id)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return SessionDetailResponse(
        session_id=session.id,
        created_at=session.created_at,
        entries=session.entries,
    )


@app.post("/api/write/generate", response_model=WriteResponse)
def generate(request: WriteGenerateRequest, db: Session = Depends(get_db)) -> WriteResponse:
    output = ai_writer.generate(request.prompt, request.tone)
    try:
        entry = ContentService(db).add_entry(
            session_id=request.session_id,
            content_type=ContentType.GENERATED,
            input_text=request.prompt,
            output_text=output,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return WriteResponse(
        entry_id=entry.id,
        output_text=entry.output_text,
        content_type=entry.content_type,
        created_at=entry.created_at,
    )


@app.post("/api/write/edit", response_model=WriteResponse)
def edit(request: WriteEditRequest, db: Session = Depends(get_db)) -> WriteResponse:
    output = ai_writer.edit(request.text, request.instruction)
    try:
        entry = ContentService(db).add_entry(
            session_id=request.session_id,
            content_type=ContentType.EDITED,
            input_text=request.text,
            output_text=output,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return WriteResponse(
        entry_id=entry.id,
        output_text=entry.output_text,
        content_type=entry.content_type,
        created_at=entry.created_at,
    )


@app.post("/api/write/refine", response_model=WriteResponse)
def refine(request: WriteRefineRequest, db: Session = Depends(get_db)) -> WriteResponse:
    output = ai_writer.refine(request.text)
    try:
        entry = ContentService(db).add_entry(
            session_id=request.session_id,
            content_type=ContentType.REFINED,
            input_text=request.text,
            output_text=output,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return WriteResponse(
        entry_id=entry.id,
        output_text=entry.output_text,
        content_type=entry.content_type,
        created_at=entry.created_at,
    )
