from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.services import chat_service
from backend.app.utils.logger import get_logger

settings = get_settings()
logger = get_logger("backend")

app = FastAPI(title=settings.APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.APP_NAME}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        conversation_id, answer, latency_ms, model_name = await chat_service.handle_chat(
            request.message, request.conversation_id, request.user_id
        )
    except (RuntimeError, ValueError) as exc:
        logger.warning(
            "Chat generation failed: %s",
            str(exc),
            extra={"conversation_id": request.conversation_id},
        )
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - safety net
        logger.exception(
            "Unexpected chat failure",
            extra={"conversation_id": request.conversation_id},
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    logger.info(
        "Chat handled",
        extra={
            "conversation_id": conversation_id,
            "latency_ms": latency_ms,
            "message_length": len(request.message),
        },
    )

    return ChatResponse(
        conversation_id=conversation_id,
        answer=answer,
        latency_ms=latency_ms,
        model=model_name,
    )
