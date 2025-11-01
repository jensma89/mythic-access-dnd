"""
auth_schema.py

Pydantic auth schema.
"""
from pydantic import BaseModel



class Token(BaseModel):
    """Pydantic model for Tokens."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Pydantic model for token data."""
    username: str