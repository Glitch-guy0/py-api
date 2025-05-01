from beanie import Document
from auth_service.models.auth_state import AuthState

models: list[Document] = [
    AuthState,  # type: ignore
]
