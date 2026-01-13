from __future__ import annotations

import os
import secrets

import httpx
import streamlit as st
from dotenv import load_dotenv


load_dotenv()
_BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")
BACKEND_URL = f"http://localhost:{_BACKEND_PORT}"


def _init_state() -> None:
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"usr_{secrets.token_hex(4)}"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def _reset_conversation() -> None:
    st.session_state.conversation_id = None
    st.session_state.messages = []


def main() -> None:
    st.set_page_config(page_title="DemoShop Customer Support Chatbot", page_icon="💬")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap');

        :root {
          --brand-ink: #1c1b1f;
          --brand-warm: #fff3e1;
          --brand-accent: #ff7a00;
          --brand-accent-dark: #d65f00;
          --brand-muted: #6b6b6b;
          --brand-card: rgba(255, 255, 255, 0.75);
          --brand-border: rgba(28, 27, 31, 0.12);
        }

        .stApp {
          background: radial-gradient(circle at top right, #ffe8c2 0%, #fff7ea 35%, #f8f5f0 70%);
          color: var(--brand-ink);
          font-family: "Space Grotesk", sans-serif;
        }

        .stApp, .stMarkdown, .stTextInput, .stCaption, .stChatMessage {
          color: var(--brand-ink);
        }

        section[data-testid="stSidebar"] {
          color: #ffffff;
        }

        section[data-testid="stSidebar"] * {
          color: #ffffff !important;
        }

        h1, h2, h3, h4, h5 {
          font-family: "Space Grotesk", sans-serif;
          letter-spacing: -0.02em;
        }

        .support-hero {
          background: linear-gradient(135deg, rgba(255, 122, 0, 0.18), rgba(255, 242, 225, 0.9));
          border: 1px solid var(--brand-border);
          border-radius: 18px;
          padding: 18px 22px;
          margin-bottom: 14px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }

        .support-hero h1 {
          margin: 0 0 6px 0;
          font-size: 2rem;
        }

        .support-hero p {
          margin: 0;
          color: var(--brand-muted);
        }

        .support-chip {
          display: inline-block;
          font-family: "IBM Plex Mono", monospace;
          font-size: 0.75rem;
          padding: 4px 10px;
          border-radius: 999px;
          background: var(--brand-warm);
          border: 1px solid var(--brand-border);
          margin-right: 6px;
        }

        .stChatMessage {
          border-radius: 16px;
          background: var(--brand-card);
          border: 1px solid var(--brand-border);
          padding: 6px 6px 2px 6px;
        }

        .stButton button {
          background: var(--brand-accent);
          color: #ffffff;
          border: none;
          border-radius: 999px;
          padding: 0.45rem 1rem;
          font-weight: 600;
        }

        .stButton button:hover {
          background: var(--brand-accent-dark);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="support-hero">
          <span class="support-chip">DemoShop</span>
          <span class="support-chip">Support Desk</span>
          <h1>Customer Support Chatbot</h1>
          <p>Ask about orders, refunds, shipping, or account help.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _init_state()

    with st.sidebar:
        st.subheader("Session")
        st.write(f"Conversation ID: {st.session_state.conversation_id or 'New'}")
        if st.button("Reset conversation"):
            _reset_conversation()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and message.get("latency_ms") is not None:
                st.caption(f"Latency: {message['latency_ms']} ms")

    user_input = st.chat_input("Ask a support question")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        "conversation_id": st.session_state.conversation_id,
        "user_id": st.session_state.user_id,
        "message": user_input,
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = httpx.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError:
                st.error("The backend is unreachable or returned an error.")
                return

            st.session_state.conversation_id = data.get("conversation_id")
            assistant_reply = data.get("answer", "")
            latency_ms = data.get("latency_ms")
            st.write(assistant_reply)
            if latency_ms is not None:
                st.caption(f"Latency: {latency_ms} ms")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply,
                    "latency_ms": latency_ms,
                }
            )


if __name__ == "__main__":
    main()
