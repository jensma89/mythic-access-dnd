"""
user_service_exceptions.py

Custom exceptions for user services.
"""


class UserServiceError(Exception):
    """Base exception for UserService errors."""
    pass


class UserNotFoundError(UserServiceError):
    """Raised when a user is not found."""
    pass


class UserCreateError(UserServiceError):
    """Raised when creating a user fails."""
    pass


class UserUpdateError(UserServiceError):
    """Raised when updating a user fails."""
    pass


class UserDeleteError(UserServiceError):
    """Raised when deleting a user fails"""
    pass
