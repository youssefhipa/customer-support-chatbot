from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv


TARGET_COUNT = 100

_templates = [
    "Where is my order {order}?",
    "I want a refund for order {order}.",
    "Reset my password for account {num}.",
    "I'm very angry about order {order}.",
    "Do you store my credit card information?",
    "Can I change the delivery address for order {order}?",
    "What is the shipping time to France for order {order}?",
    "I want to return order {order}.",
    "Please cancel order {order}.",
    "My tracking number for order {order} does not work.",
    "I never received my confirmation email for order {order}.",
    "The product from order {order} arrived damaged.",
    "I want to exchange an item from order {order}.",
    "How do I start a warranty claim for item {num}?",
    "Can you resend the invoice for order {order}?",
    "What is your return window?",
    "My order {order} shows delivered but I did not get it.",
    "Do you support PayPal for order {order}?",
    "Is international shipping available to Switzerland?",
    "I need proof of purchase for order {order}.",
]

PROMPTS: list[str] = []
seen: set[str] = set()
idx = 0
while len(PROMPTS) < TARGET_COUNT:
    order_number = f"DS-{100000 + idx:06d}"
    candidate = _templates[idx % len(_templates)].format(
        order=order_number,
        num=1000 + idx,
    )
    if candidate in seen:
        candidate = f"{candidate} (case {idx + 1})"
    PROMPTS.append(candidate)
    seen.add(candidate)
    idx += 1


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
