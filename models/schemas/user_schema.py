"""
user_schema.py

Request/response schema for users.
"""
from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime



class UserBase(SQLModel):
    """Base User model that shares common definitions"""
    user_name: str
    email: EmailStr


class UserCreate(UserBase):
    """Model to create a user"""
    hashed_password: str


class UserUpdate(SQLModel):
    """Fields (optional) to update a user"""
    user_name: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None


class UserPublic(UserBase):
    """Model to respond public data"""
    id: int
    created_at: datetime


class UserMe(UserPublic):
    """Fields to show user data by themselves"""
    email: EmailStr
    updated_at: datetime | None = None

