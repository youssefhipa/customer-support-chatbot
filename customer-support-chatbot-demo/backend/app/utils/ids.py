from __future__ import annotations

import secrets

_TOKEN_BYTES = 4


def _token() -> str:
    return secrets.token_hex(_TOKEN_BYTES)


def new_conversation_id() -> str:
    """Return a new conversation identifier like 'conv_ab12cd34'."""

    return f"conv_{_token()}"


def new_user_id() -> str:
    """Return a new user identifier like 'usr_ab12cd34'."""

    return f"usr_{_token()}"


def new_message_id() -> str:
    """Return a new message identifier like 'msg_ab12cd34'."""

    return f"msg_{_token()}"
