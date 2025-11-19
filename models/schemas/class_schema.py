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


class ClassCreateInput(SQLModel):
    """Input model for request body."""
    name: str
    race: str
    campaign_id: int
    skills: Optional[ClassSkills] = Field(default_factory=ClassSkills)


class ClassCreate(ClassCreateInput):
    """Intern model to create a class."""
    user_id: Optional[int] = None

    def set_user(self, user_id: int):
        """Set the current user ID."""
        self.user_id = user_id


class ClassUpdate(SQLModel):
    """Model to update a existing class."""
    skills: Optional[ClassSkills] = None
    notes: Optional[str] = None
    inventory: Optional[str] = None


class ClassPublic(ClassBase):
    """Model to respond public data."""
    id: int
    user_id: int
    notes: Optional[str] = None
    inventory: Optional[str] = None
