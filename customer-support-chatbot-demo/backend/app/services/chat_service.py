from __future__ import annotations

from typing import Optional

from pathlib import Path

from backend.app.clients.proxy_client import call_chat
from backend.app.config import get_settings
from backend.app.utils import ids

_PROFILE_PATH = Path(__file__).resolve().parent.parent / "company_profile.md"
_FAQ_PATH = Path(__file__).resolve().parent.parent / "company_faq.md"


def _load_company_profile() -> str:
    """Load the company profile text for prompt injection."""

    return _PROFILE_PATH.read_text(encoding="utf-8").strip()


def _load_company_faq() -> str:
    """Load the company FAQ text for prompt injection."""

    return _FAQ_PATH.read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = (
    "You are a customer support assistant for DemoShop, a fictional online retailer. "
    "Tone: professional, calm, concise, and helpful. "
    "Do not hallucinate; if you do not know, ask a clarifying question. "
    "Never request or store payment details or passwords. "
    "If asked to perform actions you cannot do (refund execution, password reset), "
    "explain the steps and offer to connect to human support.\n\n"
    "Company profile:\n"
    f"{_load_company_profile()}\n\n"
    "Company FAQ:\n"
    f"{_load_company_faq()}\n\n"
    "Behavior rules:\n"
    "- Order tracking: ask for order number if missing; provide tracking guidance.\n"
    "- If the customer is angry, acknowledge frustration, apologize briefly, and propose "
    "next steps.\n"
    "- Out-of-scope actions: you cannot issue refunds or reset passwords directly; "
    "explain the steps and offer escalation."
)


async def handle_chat(
    message: str,
    conversation_id: Optional[str],
    user_id: Optional[str],
) -> tuple[str, str, int, str]:
    """Handle a chat request and return identifiers, answer, latency, and model."""

    settings = get_settings()
    resolved_conversation_id = conversation_id or ids.new_conversation_id()

    # Keep the payload minimal for this demo; no persistence or history.
    answer, latency_ms = await call_chat(SYSTEM_PROMPT, message)

    return resolved_conversation_id, answer, latency_ms, settings.MODEL_NAME
