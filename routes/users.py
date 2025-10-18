"""
users.py

The API endpoints for users.
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import SessionDep
from models.schemas.user_schema import *
from repositories.sql_user_repository import SqlAlchemyUserRepository
from services.user_service import UserService


router = APIRouter(tags=["users"])


async def get_user_service(session: SessionDep) -> UserService:
    """Factory to get the user service."""
    repo = SqlAlchemyUserRepository(session)
    return UserService(repo)


@router.get("/users/",
            response_model=List[UserPublic])
async def read_users(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        service: UserService = Depends(get_user_service)):
    """Endpoint to get all users."""
    return service.list_users(offset, limit)


@router.post("/users/",
             response_model=UserPublic)
async def create_user(
        user: UserCreate,
        service: UserService = Depends(get_user_service)):
    """Endpoint to create a new user."""
    return service.create_user(user)


@router.put("/users/{user_id}",
            response_model=UserPublic)
async def update_user(
        user_id: int,
        user: UserUpdate,
        service: UserService = Depends(get_user_service)):
    """Endpoint to change user data."""
    updated = service.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return updated


@router.delete("/users/{user_id}",
               response_model=UserPublic)
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service)):
    """Endpoint to delete a user by id."""
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return deleted
