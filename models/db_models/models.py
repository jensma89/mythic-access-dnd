"""
models.py

Table models for DB.
"""
from sqlmodel import Field, SQLModel, select
from pydantic import EmailStr
from datetime import datetime, timezone



class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

