from typing import Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    topic: Optional[str] = None
    year: Optional[int] = None
    mode: str = "qa"
    session_id: Optional[str] = None


class Source(BaseModel):
    document: str
    source: str
    topic: Optional[str] = None
    year: Optional[int] = None


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class CreateSessionResponse(BaseModel):
    session_id: str


class DeleteSessionResponse(BaseModel):
    message: str