# app/utils/exceptions.py
"""
Custom HTTP exceptions for the API.
"""

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """
    Exception raised when a resource is not found.
    Returns 404 status code.
    """
    
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found"
        )


class ValidationException(HTTPException):
    """
    Exception raised when business validation fails.
    Returns 400 status code.
    """

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ConflictException(HTTPException):
    """
    Exception raised when a resource conflict occurs (e.g. duplicate entry).
    Returns 409 status code.
    """

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
