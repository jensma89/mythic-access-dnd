"""
auth_service.py

Business logic for authentication (register, login, hashing, token creation).
"""
from datetime import timedelta
from fastapi import HTTPException
from sqlmodel import Session, select
from models.db_models.table_models import User
from models.schemas.user_schema import UserCreate
from models.schemas.auth_schema import Token
from auth.auth import (
    hash_password,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
import logging



logger = logging.getLogger(__name__)


class AuthService:

    def register_user(self, session:Session, user_data: UserCreate) -> User:
        """Register a new user: check duplicates, hash password, store user."""
        existing = session.exec(
            select(User).where(
                (User.email == user_data.email) |
                (User.user_name == user_data.user_name)
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="A user with that email or username already exists."
            )

        db_user = User(
            user_name=user_data.user_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


    def login(self, session: Session, login: str, password: str) -> Token:
        """Authenticate user and issue access token."""
        user= authenticate_user(
            session=session,
            login=login,
            password=password
        )
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user.email},
            expires_delta=expires
        )
        return Token(access_token=token, token_type="bearer")
