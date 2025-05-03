from beanie import Document
from models.auth_state import AuthState

models: list[Document] = [
    AuthState,  # type: ignore
]
