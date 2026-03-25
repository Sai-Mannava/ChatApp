from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ContentType


class SessionCreateResponse(BaseModel):
    session_id: str


class WriteGenerateRequest(BaseModel):
    session_id: str
    prompt: str = Field(min_length=5, max_length=4000)
    tone: str = Field(default="professional", min_length=2, max_length=60)


class WriteEditRequest(BaseModel):
    session_id: str
    text: str = Field(min_length=5, max_length=4000)
    instruction: str = Field(min_length=3, max_length=500)


class WriteRefineRequest(BaseModel):
    session_id: str
    text: str = Field(min_length=5, max_length=4000)


class WriteResponse(BaseModel):
    entry_id: str
    output_text: str
    content_type: ContentType
    created_at: datetime


class SessionEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content_type: ContentType
    input_text: str
    output_text: str
    created_at: datetime


class SessionDetailResponse(BaseModel):
    session_id: str
    created_at: datetime
    entries: list[SessionEntry]
