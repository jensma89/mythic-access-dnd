"""
class_service_exceptions.py

Custom exceptions for dnd_class services.
"""


class ClassServiceError(Exception):
    """Base exception for ClassService errors."""
    pass


class ClassNotFoundError(Exception):
    """Raised when a dnd_class is not found."""
    pass


class ClassCreateError(Exception):
    """Raised when creating a dnd_class fails."""
    pass


class ClassUpdateError(Exception):
    """Raised when updating a dnd_class fails."""
    pass


class ClassDeleteError(Exception):
    """Raised when deleting a dnd_class fails"""
    pass
