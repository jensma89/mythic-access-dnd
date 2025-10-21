"""
dice_schema.py

Request/response schema for dices.
"""
from sqlmodel import SQLModel
from typing import Optional



class DiceBase(SQLModel):
    """Base dice model to share common definitions."""
    id: int
    name: str
    sides: int


class DiceCreate(SQLModel):
    """Model to create a new dice."""
    name: str
    sides: int


class DiceUpdate(SQLModel):
    """Model to change the dice."""
    name: Optional[str] = None
    sides: Optional[int] = None


class DicePublic(DiceBase):
    """Model to respond public data."""


class DiceRollResult(DiceBase):
    """Model to respond the roll result."""
    result: int
