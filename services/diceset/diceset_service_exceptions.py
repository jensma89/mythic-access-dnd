"""
diceset_service_exceptions.py

Custom exceptions for dice set services.
"""


class DiceSetServiceError(Exception):
    """Base exception for DiceSetService errors."""
    pass


class DiceSetNotFoundError(DiceSetServiceError):
    """Raised when a dice set is not found."""
    pass


class DiceSetCreateError(DiceSetServiceError):
    """Raised when creating a dice set fails."""
    pass


class DiceSetUpdateError(DiceSetServiceError):
    """Raised when updating a dice set fails."""
    pass


class DiceSetDeleteError(DiceSetServiceError):
    """Raised when deleting a dice set fails"""
    pass


class DiceSetRollError(DiceSetServiceError):
    """Raised when rolling a dice set fails."""
    pass
