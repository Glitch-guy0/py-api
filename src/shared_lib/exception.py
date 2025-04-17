from fastapi import HTTPException


class ApplicationError(HTTPException):
    """
    Base class for all application exceptions.

    details: (Optional) Specific problems — useful for form validation, etc.
    status: (Optional) HTTP status code (e.g. 400, 404) — can also be kept at HTTP level
    """

    def __init__(self, detail: str, status_code: int):
        error_message = {"error": {"detail": detail}}
        super().__init__(status_code=status_code, detail=error_message)
