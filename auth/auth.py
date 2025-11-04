"""
auth.py
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from dotenv import load_dotenv
from models.schemas.auth_schema import Token, TokenData
from models.schemas.user_schema import *
from dependencies import SessionDep
from models.db_models.table_models import User
from sqlmodel import select, Session


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


# Token functions

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a access token with expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Authentication

async def authenticate_user(
        session: Session = Depends(SessionDep),
        email: str | None = None,
        password: str | None = None):
    """Check username + password in database."""
    if email is None or password is None:
        return None
    stmt = (select(User)
            .where(User.email == email))
    user = session.exec(stmt).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Token validation

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(SessionDep)):
    """Validate JWT token and load the user from DB using email (sub)."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    stmt = (select(User)
            .where(User.email == email))
    user = session.exec(stmt).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    """Optional: map DB user to public 'me' schema
    and check active state if you have it."""
    if getattr(current_user, "disabled", False):
        raise HTTPException(
            status_code=400,
            detail="Inactive user."
        )
    return UserMe.model_validate(current_user)

