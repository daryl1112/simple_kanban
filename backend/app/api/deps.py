"""Shared FastAPI dependencies and error translation helpers.

The service layer raises domain errors (NotFoundError, ValidationError). Here
we translate them into HTTP exceptions so business logic stays HTTP-agnostic.
"""

from fastapi import HTTPException, status

from app.services.errors import NotFoundError, ValidationError


def http_error_from_domain(exc: Exception) -> HTTPException:
    """Map a domain exception to the appropriate HTTPException."""
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValidationError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    # Unknown domain error: surface as a 500 without leaking internals.
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
