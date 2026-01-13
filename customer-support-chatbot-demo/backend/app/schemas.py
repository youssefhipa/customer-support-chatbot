from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming user chat payload."""

    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    """Structured response returned to the client."""

    conversation_id: str
    answer: str
    latency_ms: int
    model: str
