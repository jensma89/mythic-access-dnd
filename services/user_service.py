"""
user_service.py

Business logic for user.
"""
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from dependencies import UserQueryParams
from models.schemas.user_schema import *
from repositories.user_repository import UserRepository
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository
import logging



logger = logging.getLogger(__name__)


class UserService:
    """Initialise the business logic
    for user service operations."""
    def __init__(self,
                 user_repo: UserRepository,
                 campaign_repo: CampaignRepository,
                 class_repo: ClassRepository,
                 diceset_repo: DiceSetRepository,
                 dicelog_repo: DiceLogRepository):
        self.user_repo = user_repo
        self.campaign_repo = campaign_repo
        self.class_repo = class_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo
        logger.debug("UserService initialized with repositories")


    def create_user(self, user: UserCreate) \
            -> UserPublic:
        """Create a new user."""
        try:
            created_user = self.user_repo.add(user)
            if not created_user:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create User."
                )
            logger.error("Database error while creating user", exc_info=True)
            return created_user
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while creating user."
            )


    def get_user(self, user_id: int) \
            -> Optional[UserPublic]:
        """Get a user by id."""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                logger.warning(f"User {user_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"User with user ID "
                           f"{user_id} not found."
                )
            logger.debug(f"Retrieved User {user_id}")
            return user
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while retrieving user."
            )


    def list_users(self,
                   filters: UserQueryParams,
                   offset: int = 0,
                   limit: int = 100
                   ) -> List[UserPublic]:
        """Get a list of all users."""
        try:
            users = self.user_repo.list_all(
                name=filters.name,
                offset=offset,
                limit=limit
            )
            logger.debug(f"Listed {len(users)} users with filter name={filters.name}")
            return users
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while listing users."
            )


    def update_user(self,
                    user_id: int,
                    user: UserUpdate) \
            -> Optional[UserPublic]:
        """Make changes by a user."""
        try:
            existing = self.user_repo.get_by_id(user_id)
            if not existing:
                logger.warning(f"Attempted update on non-existing User {user_id}")
                raise HTTPException(
                    status_code=404,
                    detail=f"User with ID {user_id} "
                           f"not found"
                )

            updated_user =self.user_repo.update(user_id, user)
            if not updated_user:
                logger.error("Database error while updating user", exc_info=True)
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update user."
                )
            logger.info(f"Updated User {user_id}")
            return updated_user
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while updating user."
            )


    def delete_user(self, user_id: int) -> Optional[UserPublic]:
        """Delete a user and the belonging campaign,
        classes, dice sets and logs."""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                logger.warning(f"Attempted delete a non-existing user {user_id}. ")
                raise HTTPException(
                    status_code=404,
                    detail=f"User with ID {user_id} "
                           f"not found."
                )

            # Delete dice logs
            for log in (self.dicelog_repo
                    .list_by_user(user_id)):
                self.dicelog_repo.delete(log.id)
                logger.info(f"Deleted DiceLog {log.id} for User {user_id}")

            # Delete dice sets
            for diceset in (self.diceset_repo
                    .list_by_user(user_id)):
                self.diceset_repo.delete(diceset.id)
                logger.info(f"Deleted DiceSet {diceset.id} for User {user_id}")

            # Delete classes
            for dnd_class in (self.class_repo
                    .list_by_user(user_id)):
                self.class_repo.delete(dnd_class.id)
                logger.info(f"Deleted DnDClass {dnd_class.id} for User {user_id}")

            # Delete campaigns
            for campaign in (self.campaign_repo
                    .list_by_user(user_id)):
                self.campaign_repo.delete(campaign.id)
                logger.info(f"Deleted Campaign {campaign.id} for User {user_id}")

            # Finally delete user
            deleted_user = self.user_repo.delete(user_id)
            if not deleted_user:
                logger.error(f"Failed to delete User {user_id}")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete user."
                )
            logger.info(f"Deleted User {user_id} - {deleted_user.user_name}")
            return deleted_user
        except SQLAlchemyError:
            logger.error(f"Database error while deleting User {user_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while deleting user."
            )
        except Exception:
            logger.error(f"Unexpected error while deleting User {user_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error "
                       f"while deleting user.")
