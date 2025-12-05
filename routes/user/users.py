"""
users.py

The API endpoints for users.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Request

from dependencies import Pagination, SessionDep, UserQueryParams
from models.db_models.table_models import User
from models.schemas.user_schema import UserUpdate, UserPublic
from repositories.sql_user_repository import SqlAlchemyUserRepository
from services.user.user_service import UserService
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from auth.auth import get_current_user
from rate_limit import limiter
import logging

from services.user.user_service_exceptions import UserNotFoundError

router = APIRouter(tags=["users"])
logger = logging.getLogger(__name__)


def get_user_service(session: SessionDep) \
        -> UserService:
    """Factory to get the user, campaign,
    dnd_class, dice set and dice log service."""
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
@limiter.limit("10/minute")
def read_user(
        request: Request,
        user_id: int = Path(..., description="The ID of the user to retrieve"),
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)):
    """Endpoint to get a single user."""
    logger.debug(f"GET /users/{user_id} requested")
    try:
        user = service.get_user(user_id)
        return user
    except UserNotFoundError:
        logger.warning(f"User {user_id} not found.")
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    except Exception:
        logger.error(
            f"Unexpected error while "
            f"retrieving User {user_id}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )


@router.get("/users/",
            response_model=List[UserPublic])
@limiter.limit("10/minute")
def read_users(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        filters: UserQueryParams = Depends(),
        service: UserService = Depends(get_user_service)):
    """Endpoint to get all users."""
    logger.debug("GET /users/ list requested")
    return service.list_users(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters)


@router.patch("/users/me/update",
            response_model=UserPublic)
@limiter.limit("3/minute")
def update_user(
        request: Request,
        user: UserUpdate,
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)):
    """Update the currently authenticated user."""
    logger.debug(f"PATCH /users/me/update update requested by user {current_user.id}")

    updated = service.update_user(current_user.id, user)

    if not updated:
        logger.error(
            f"Update failed, "
            f"User {current_user.id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="User not found")
    logger.info(
        f"User {current_user.id} "
        f"updated successfully."
    )
    return updated


@router.delete("/users/me/delete",
               response_model=UserPublic)
@limiter.limit("3/minute")
def delete_user(
        request: Request,
        current_user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
):
    """Delete the authenticated user + all related resources."""
    logger.warning(f"DELETE /users/me/delete requested by user {current_user.id}")

    deleted = service.delete_user(current_user.id)

    if not deleted:
        logger.error(f"Delete failed, User {current_user.id} not found")
        raise HTTPException(
            status_code=404,
            detail="User not found")
    logger.info(f"User {current_user.id} and all related data deleted.")
    return deleted
