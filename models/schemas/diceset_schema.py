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


class DiceSetCreateInput(SQLModel):
    """Model to create a dice set (Request body input)."""
    name: str
    dnd_class_id: int
    campaign_id: int
    dice_ids: Optional[List[int]] = None # IDs that contain in a dice set


class DiceSetCreate(DiceSetCreateInput):
    """Intern model to create a dice set."""
    user_id: Optional[int] = None

    def set_user(self, user_id: int, ):
        """Set the ID from current user."""
        self.user_id = user_id


class DiceSetUpdate(SQLModel):
    """Model to update a dice set."""
    name: Optional[str] = None
    dice_ids: Optional[List[int]] = None


class DiceSetPublic(DiceSetBase):
    """Model to respond public data."""
    id: int
    user_id: int
    dices: List[DicePublic]


class DiceSetRollResult(SQLModel):
    """Model to respond the data after roll a dice set."""
    diceset_id: int
    name: str
    results: List[DiceRollResult]
    total: int
