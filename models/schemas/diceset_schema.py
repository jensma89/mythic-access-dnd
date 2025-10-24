"""
diceset_schema.py

Request/response schema for dice sets.
"""
from sqlmodel import SQLModel
from typing import List, Optional
from models.schemas.dice_schema import DicePublic, DiceRollResult


class DiceSetBase(SQLModel):
    """Base model for dice sets
    to share common definitions."""
    name: str


class DiceSetCreate(SQLModel):
    """Model to create a dice set."""
    name: str
    class_id: int
    campaign_id: int
    dice_ids: Optional[List[int]] = None # IDs that contain in a dice set


class DiceSetUpdate(SQLModel):
    """Model to update a dice set."""
    name: Optional[str] = None
    dice_ids: Optional[List[int]] = None


class DiceSetPublic(DiceSetBase):
    """Model to respond public data."""
    id: int
    dices: Optional[List[DicePublic]]


class DiceSetRollResult(SQLModel):
    """Model to respond the data after roll a dice set."""
    diceset_id: int
    name: str
    results: List[DiceRollResult]
    total: int
