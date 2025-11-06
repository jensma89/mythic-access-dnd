"""
dicelog_schema.py

Request/response schema for dice logs.
"""
from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime



class DiceLogBase(SQLModel):
    """Base model for dice logs
        to share common definitions."""
    user_id: int
    campaign_id: int
    class_id: int
    diceset_id: int | None = None
    roll: str
    result: int


class DiceLogCreate(DiceLogBase):
    """Model to create a new dice log."""
    pass


class DiceLogPublic(DiceLogBase):
    """Model to respond public data."""
    id: int
    timestamp: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
