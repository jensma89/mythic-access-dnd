"""
users.py

The API endpoints for users.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from dependencies import Pagination, SessionDep, UserQueryParams
from models.schemas.user_schema import *
from repositories.sql_user_repository import SqlAlchemyUserRepository
from services.user_service import UserService
from services.campaign_service import CampaignService
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository



router = APIRouter(tags=["users"])


async def get_user_service(session: SessionDep) -> UserService:
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
async def read_user(
        user_id: int,
        service: UserService = Depends(get_user_service)):
    """Endpoint to get a single user."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found.")
    return user


@router.get("/users/",
            response_model=List[UserPublic])
async def read_users(
        pagination: Pagination = Depends(),
        filters: UserQueryParams = Depends(),
        service: UserService = Depends(get_user_service)):
    """Endpoint to get all users."""
    return service.list_users(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters)


@router.post("/users/",
             response_model=UserPublic)
async def create_user(
        user: UserCreate,
        service: UserService = Depends(get_user_service)):
    """Endpoint to create a new user."""
    return service.create_user(user)


@router.patch("/users/{user_id}",
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
