"""
user_service_exceptions.py

Custom exceptions for user services.
"""


class UserServiceError(Exception):
    """Base exception for UserService errors."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass


class UserCreateError(Exception):
    """Raised when creating a user fails."""
    pass


class UserUpdateError(Exception):
    """Raised when updating a user fails."""


class UserDeleteError(Exception):
    """Raised when deleting a user fails"""
