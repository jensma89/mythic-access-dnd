"""
auth_schema.py

JWT-related auth schemas: login requests and tokens.
"""
from pydantic import BaseModel



class Token(BaseModel):
    """Token base model."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str
