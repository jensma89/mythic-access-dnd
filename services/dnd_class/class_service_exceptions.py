"""
class_service_exceptions.py

Custom exceptions for dnd_class services.
"""


class ClassServiceError(Exception):
    """Base exception for ClassService errors."""
    pass


class ClassNotFoundError(ClassServiceError):
    """Raised when a dnd_class is not found."""
    pass


class ClassCreateError(ClassServiceError):
    """Raised when creating a dnd_class fails."""
    pass


class ClassUpdateError(ClassServiceError):
    """Raised when updating a dnd_class fails."""
    pass


class ClassDeleteError(ClassServiceError):
    """Raised when deleting a dnd_class fails"""
    pass
