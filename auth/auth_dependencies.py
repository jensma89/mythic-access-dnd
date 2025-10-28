"""
auth_dependencies.py

Dependencies to compare if its current user.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from auth.jwt import decode_access_token
from repositories.sql_user_repository import SqlAlchemyUserRepository
from dependencies import SessionDep



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep
):
    """Compare if token is current user."""
    payload = decode_access_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    user_repo = SqlAlchemyUserRepository(session)
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return user
