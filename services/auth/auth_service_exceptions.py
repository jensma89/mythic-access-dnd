"""
auth_service_exceptions.py

Custom exceptions for auth services.
"""

class AuthServiceError(Exception):
    """Base exception for all
    AuthService-related failures."""
    pass


class UserAlreadyExistsError(AuthServiceError):
    """Raised when trying to
    register a user that already exists."""
    pass


class InvalidCredentialsError(AuthServiceError):
    """Raised when login credentials are incorrect."""
    pass


class TokenCreationError(AuthServiceError):
    """Raised when generating a token fails."""
    pass
