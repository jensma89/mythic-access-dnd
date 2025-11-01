"""
auth.py
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from dotenv import load_dotenv
from schemas.auth_schema import Token, TokenData
from schemas.user_schema import *
from dependencies import SessionDep
from models.db_models.table_models import User
from sqlmodel import select


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Password functions

def hash_password(password: str):
    """Hash a plain password."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verify a plain with hashed password."""
    return password_hash.verify(plain_password, hashed_password)


