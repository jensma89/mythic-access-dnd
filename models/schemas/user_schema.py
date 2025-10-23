"""
user_schema.py

Request/response schema for users.
"""
from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime
from typing import Optional



class UserBase(SQLModel):
    """Base User model that shares common definitions."""
    user_name: str


class UserCreate(SQLModel):
    """Model to create a user."""
    user_name: str
    email: EmailStr
    hashed_password: str


class UserUpdate(SQLModel):
    """Fields (optional) to update a user."""
    user_name: Optional[str] = None
    email: Optional[EmailStr]  = None
    hashed_password: Optional[str] = None


class UserPublic(UserBase):
    """Model to respond public data."""
    id: int
    created_at: datetime

    class Config:
        """Formatted timestamp."""
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


class UserMe(UserPublic):
    """Fields to show user data by themselves."""
    email: EmailStr
    updated_at: datetime | None = None

    class Config(UserPublic.Config):
        """Formatting timestamp get config from UserPublic.Config."""
        pass
