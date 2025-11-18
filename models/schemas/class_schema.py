"""
class_schema.py

Request/response schema for classes.
"""
from sqlmodel import Field, SQLModel
from typing import Optional



class ClassSkills(SQLModel):
    """Skills model for attribute-based systems."""
    Constitution: int = 0
    Strength: int = 0
    Stamina: int = 0
    Dexterity: int = 0
    Wisdom: int = 0
    Intelligence: int = 0
    Charisma: int = 0


class ClassBase(SQLModel):
    """Base Class model that shares common definitions."""
    name: str
    race: str
    skills: ClassSkills


class ClassCreate(SQLModel):
    """Model to create a class."""
    name: str
    race: str
    campaign_id: int
    skills: Optional[ClassSkills] = Field(default_factory=ClassSkills)


class ClassUpdate(SQLModel):
    """Model to update a existing class."""
    skills: Optional[ClassSkills] = None
    notes: Optional[str] = None
    inventory: Optional[str] = None


class ClassPublic(ClassBase):
    """Model to respond public data."""
    id: int
    notes: Optional[str] = None
    inventory: Optional[str] = None
