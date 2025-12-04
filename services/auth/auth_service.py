"""
auth_service.py

Business logic for authentication (register, login, hashing, token creation).
"""
from datetime import timedelta
from sqlmodel import Session, select
import logging

from models.db_models.table_models import User
from models.schemas.user_schema import UserCreate
from models.schemas.auth_schema import Token
from services.auth.auth_service_exceptions import *
from auth.auth import (
    hash_password,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)



logger = logging.getLogger(__name__)


class AuthService:

    def register_user(
            self,
            session:Session,
            user_data: UserCreate
    ) -> User:
        """Register a new user:
        check duplicates, hash password, store user."""
        try:
            existing = session.exec(
                select(User).where(
                    (User.email == user_data.email) |
                    (User.user_name == user_data.user_name)
                )
            ).first()

        except Exception:
            logger.error(
                "Error while registering user",
                exc_info=True
            )
            raise AuthServiceError(
                "Error while checking duplicates"
            )
        if existing:
            raise UserAlreadyExistsError(
                "A user with that email "
                "or username already exists."
            )
        try:
            db_user = User(
                user_name=user_data.user_name,
                email=user_data.email,
                hashed_password=hash_password(
                    user_data.password
                )
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

        except Exception:
            logger.error(
                "Error while creating new user",
                exc_info=True
            )
            raise AuthServiceError(
                "Error while storing user."
            )


    def login(
            self,
            session: Session,
            login: str,
            password: str
    ) -> Token:
        """Authenticate user and issue access token."""
        try:
            user= authenticate_user(
                session=session,
                login=login,
                password=password
            )

        except Exception:
            logger.error(
                "Error while during authentication",
                exc_info=True
            )
            raise AuthServiceError(
                "Error while during authentication."
            )

        if not user:
            raise InvalidCredentialsError(
                "Incorrect email or password"
            )

        try:
            expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            token = create_access_token(
                data={"sub": user.email},
                expires_delta=expires
            )
            return Token(access_token=token, token_type="bearer")

        except Exception:
            logger.error(
                "Token creation failed",
                exc_info=True
            )
            raise TokenCreationError(
                "Failed to create access token."
            )
