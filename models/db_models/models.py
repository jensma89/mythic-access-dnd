"""
models.py

Table models for DB.
"""
from markdown_it.rules_block import table
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint
from pydantic import EmailStr
from datetime import datetime, timezone
from typing import List, Optional



class User(SQLModel, table=True):
    """Model to create user table."""
    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

    # Relationship to campaign
    campaigns: List["Campaign"] = Relationship(back_populates="creator")


class Campaign(SQLModel, table=True):
    """Model to create a campaign table."""
    __table_args__ = (
        UniqueConstraint("title",
                         "created_by",
                         name="uq_user_title"),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str
    genre: str | None = None
    description: str | None = Field(default=None, description="Story of the campaign")
    max_classes: int
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ORM link to User
    creator: Optional[User] = Relationship(back_populates="campaigns")


class Class(SQLModel, table=True):
    pass


class DiceSet(SQLModel, table=True):
    pass


class Dice(SQLModel, table=True):
    pass


class DiceLog(SQLModel, table=True):
    pass
