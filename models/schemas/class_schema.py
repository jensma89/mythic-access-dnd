"""
class_schema.py

Request/response schema for classes.
"""
from sqlmodel import Field, SQLModel
from typing import Dict, Optional



class ClassBase(SQLModel):
    """Base Class model that shares common definitions."""
    id: int
    name: str
    race: str
    skills: Dict[str, int]


class ClassCreate(SQLModel):
    """Model to create a class."""
    name: str
    race: str
    skills: Optional[Dict[str, int]] = Field(
        default_factory=lambda: {
            "Strength": 0,
            "Stamina": 0,
            "Dexterity": 0,
            "Intelligence": 0,
            "Charisma": 0
        }
    )


class ClassUpdate(SQLModel):
    """Model to update a existing class."""
    skills: Optional[Dict[str, int]] = None
    notes: Optional[str] = None
    inventory: Optional[str] = None


class ClassPublic(SQLModel):
    """Model to respond public data."""
    name: str
    race: str
    skills: Dict[str, int]


class ClassMe(ClassBase):
    """Fields to show class data by themselves."""
    notes: str
    inventory: str
    campaign_id: int
