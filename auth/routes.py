"""
routes.py

Signup, login and user me routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from auth_schemas import *
from auth.jwt import create_access_token
from utils import hash_password, verify_password
from repositories.sql_user_repository import SqlAlchemyUserRepository
from dependencies import SessionDep


router = APIRouter(tags=["auth"])


@router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserLogin, session: SessionDep):
    """Route to register a new user."""
    repo = SqlAlchemyUserRepository(session)
    existing = repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_pw = hash_password(user_data.password)
    new_user = repo.add_user_secure(user_data.email, hashed_pw)

    token = create_access_token({"sub": new_user.email})
    return Token(access_token=token)


@router.post("/auth/login",
             response_model=Token)
async def login(
        user_data: UserLogin,
        session: SessionDep):
    """Verify a user by password password and token."""
    repo = SqlAlchemyUserRepository(session)
    user = repo.get_by_email(user_data.email)

    if not user or not verify_password(
            user_data.password,
            user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )
    access_token = create_access_token(
        {"sub": user.email},
        timedelta(minutes=60)
    )
    return Token(access_token=access_token)


@router.get("/auth/me",
            response_model=dict)
async def get_me(current_user=Depends()): # later get_current_user
    """User me for private information
    about current user"""
    return {"email": current_user.email,
            "user_name": current_user.user_name}
