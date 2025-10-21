"""
dicelog_schema.py

Request/response schema for dice logs.
"""
from sqlmodel import SQLModel
from datetime import datetime



class DiceLogBase(SQLModel):
    """Base model for dice logs
        to share common definitions."""
    user_id: int
    campaign_id: int
    roll: str
    result: int


class DiceLogCreate(DiceLogBase):
    """Model to create a new dice log."""
    pass


class DiceLogPublic(DiceLogBase):
    """Model to respond public data."""
    id: int
    timestamp = datetime
