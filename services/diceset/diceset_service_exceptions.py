"""
diceset_service_exceptions.py

Custom exceptions for dice set services.
"""


class DiceSetServiceError(Exception):
    """Base exception for DiceSetService errors."""
    pass


class DiceSetNotFoundError(Exception):
    """Raised when a dice set is not found."""
    pass


class DiceSetCreateError(Exception):
    """Raised when creating a dice set fails."""
    pass


class DiceSetUpdateError(Exception):
    """Raised when updating a dice set fails."""
    pass


class DiceSetDeleteError(Exception):
    """Raised when deleting a dice set fails"""
    pass


class DiceSetRollError(Exception):
    """Raised when rolling a dice set fails."""
    pass
