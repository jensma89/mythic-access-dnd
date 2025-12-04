"""
dice_service_exceptions.py

Custom exceptions for dice services.
"""


class DiceServiceError(Exception):
    """Base exception for DiceService errors."""
    pass


class DiceNotFoundError(Exception):
    """Raised when a dice is not found."""
    pass


class DiceCreateError(Exception):
    """Raised when creating a dice fails."""
    pass


class DiceUpdateError(Exception):
    """Raised when updating a dice fails."""
    pass


class DiceDeleteError(Exception):
    """Raised when deleting a dice fails"""
    pass


class DiceRollError(Exception):
    """Raised when roll a dice fails."""
    pass
