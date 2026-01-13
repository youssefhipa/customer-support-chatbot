from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv


PROMPTS = [
    "Where is my order?",
    "I want a refund",
    "Reset my password",
    "I'm very angry, your service is bad",
    "Do you store my credit card?",
]


def main() -> None:
    load_dotenv()
    port = os.getenv("BACKEND_PORT", "8000")
    base_url = f"http://localhost:{port}"

    conversation_id = None
    user_id = "quick_test_user"

    for prompt in PROMPTS:
        payload = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message": prompt,
        }
        response = httpx.post(f"{base_url}/chat", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        conversation_id = data.get("conversation_id")

        answer = data.get("answer")
        latency_ms = data.get("latency_ms")
        print("-")
        print(f"conversation_id: {conversation_id}")
        print(f"answer: {answer}")
        print(f"latency_ms: {latency_ms}")


if __name__ == "__main__":
    main()
