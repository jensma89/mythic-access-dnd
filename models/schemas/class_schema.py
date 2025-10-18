"""
class_schema.py

Request/response schema for classes.
"""
from sqlmodel import Field, SQLModel
from typing import Dict, Optional



class ClassSkills(SQLModel):
    """Skills model for attribute-based systems."""
    Strength: int = 0
    Stamina: int = 0
    Dexterity: int = 0
    Intelligence: int = 0
    Charisma: int = 0


class ClassBase(SQLModel):
    """Base Class model that shares common definitions."""
    id: int
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


class ClassPublic(SQLModel):
    """Model to respond public data."""
    name: str
    race: str
    skills: ClassSkills


class ClassMe(ClassBase):
    """Fields to show class data by themselves."""
    notes: str
    inventory: str
    campaign_id: int
