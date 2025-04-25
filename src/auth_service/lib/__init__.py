import secrets


def state_token_generator() -> str:
    return secrets.token_urlsafe(24)


def session_key_generator() -> str:
    return secrets.token_urlsafe(24)
