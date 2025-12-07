"""
dice_schema.py

Request/response schema for dices.
"""
from sqlmodel import SQLModel
from typing import Optional



class DiceBase(SQLModel):
    """Base dice model to share common definitions."""
    name: str
    sides: int


class DiceCreate(DiceBase):
    """Model to create a new dice."""
    pass


class DiceUpdate(SQLModel):
    """Model to change the dice."""
    name: Optional[str] = None
    sides: Optional[int] = None


class DicePublic(DiceBase):
    """Model to respond public data."""
    id: int


class DiceRollResult(DicePublic):
    """Model to respond the roll result."""
    name: str
    result: int
    sides: int
