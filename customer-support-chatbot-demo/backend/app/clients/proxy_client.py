from __future__ import annotations

from typing import Any
import time

import httpx

from backend.app.config import get_settings


async def call_chat(system_prompt: str, user_message: str) -> tuple[str, int]:
    """Call an OpenAI-compatible chat endpoint and return (answer, latency_ms)."""

    settings = get_settings()
    url = f"{settings.PROXY_BASE_URL.rstrip('/')}/{settings.PROXY_CHAT_PATH.lstrip('/')}"
    # Force identity encoding in case the proxy mislabels compressed responses.
    headers = {"Content-Type": "application/json", "Accept-Encoding": "identity"}
    if settings.PROXY_API_KEY:
        headers["Authorization"] = f"Bearer {settings.PROXY_API_KEY}"

    payload = {
        "model": settings.MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }

    timeout = httpx.Timeout(settings.REQUEST_TIMEOUT_SECONDS)
    start = time.monotonic()
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
    latency_ms = int((time.monotonic() - start) * 1000)

    if response.is_error:
        raise RuntimeError(
            f"Upstream error {response.status_code}: {response.text}"
        )

    data: dict[str, Any] = response.json()
    try:
        content = data["choices"][0]["message"]["content"]
        return str(content).strip(), latency_ms
    except (KeyError, IndexError, TypeError) as exc:
        snippet = response.text[:200].replace("\n", " ")
        raise ValueError(
            f"Unexpected proxy response format. Snippet: {snippet}"
        ) from exc
