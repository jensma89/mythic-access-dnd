"""
auth_schema.py

JWT-related auth schemas: login requests and tokens.
"""
from sqlmodel import SQLModel



class UserLogin(SQLModel):
    """User login credentials."""
    user_name: str
    password: str


class Token(SQLModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
