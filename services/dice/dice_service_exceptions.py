"""
dice_service_exceptions.py

Custom exceptions for dice services.
"""


class DiceServiceError(Exception):
    """Base exception for DiceService errors."""
    pass


class DiceNotFoundError(DiceServiceError):
    """Raised when a dice is not found."""
    pass


class DiceCreateError(DiceServiceError):
    """Raised when creating a dice fails."""
    pass


class DiceUpdateError(DiceServiceError):
    """Raised when updating a dice fails."""
    pass


class DiceDeleteError(DiceServiceError):
    """Raised when deleting a dice fails"""
    pass


class DiceRollError(DiceServiceError):
    """Raised when rolling a dice fails."""
    pass
