from fastapi import HTTPException


class ApplicationError(HTTPException):
    """
    Base class for all application exceptions.

    code: A short machine-readable identifier (e.g. invalid_request, unauthorized, not_found)
    message: Human-readable error description. Should be clear and concise.
    details: (Optional) Specific problems — useful for form validation, etc.
    status: (Optional) HTTP status code (e.g. 400, 404) — can also be kept at HTTP level
    timestamp: (Optional) Useful for logging and debugging.
    request_id: (Optional) If using tracing/logs — helps match logs with errors.
    """

    def __init__(self, detail: str, status_code: int):
        error_message = {"error": {"detail": detail}}
        super().__init__(status_code=status_code, detail=error_message)
