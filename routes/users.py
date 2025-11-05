"""
users.py

The API endpoints for users.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException,Path ,Query
from dependencies import Pagination, SessionDep, UserQueryParams
from models.db_models.table_models import User
from models.schemas.user_schema import (UserCreate,
                                        UserUpdate,
                                        UserPublic)
from repositories.sql_user_repository import SqlAlchemyUserRepository
from services.user_service import UserService
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from auth.auth import get_current_user



router = APIRouter(tags=["users"])


def get_user_service(session: SessionDep) \
        -> UserService:
    """Factory to get the user, campaign,
    class, dice set and dice log service."""
    user_repo = SqlAlchemyUserRepository(session)
    campaign_repo = SqlAlchemyCampaignRepository(session)
    class_repo = SqlAlchemyClassRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)
    dicelog_repo = SqlAlchemyDiceLogRepository(session)
    return UserService(user_repo,
                       campaign_repo,
                       class_repo,
                       diceset_repo,
                       dicelog_repo)


@router.get("/users/{user_id}",
            response_model=UserPublic)
def read_user(
        user_id: int = Path(..., description="The ID of the user to retrieve"),
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)):
    """Endpoint to get a single user."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.")
    return user


@router.get("/users/",
            response_model=List[UserPublic])
def read_users(
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        filters: UserQueryParams = Depends(),
        service: UserService = Depends(get_user_service)):
    """Endpoint to get all users."""
    return service.list_users(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters)


@router.patch("/users/{user_id}",
            response_model=UserPublic)
def update_user(
        user: UserUpdate,
        user_id: int = Path(..., description="The ID of the user to update."),
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)):
    """Endpoint to change user data."""
    updated = service.update_user(user_id, user)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return updated


@router.delete("/users/{user_id}",
               response_model=UserPublic)
def delete_user(
        user_id: int = Path(..., description="The ID of the user to delete."),
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)):
    """Endpoint to delete a user by id."""
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return deleted
