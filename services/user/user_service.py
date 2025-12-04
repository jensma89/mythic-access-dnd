"""
user_service.py

Business logic for user.
"""
import logging
from typing import List

from dependencies import UserQueryParams
from models.schemas.user_schema import *
from repositories.user_repository import UserRepository
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository
from services.user.user_service_exceptions import *



logger = logging.getLogger(__name__)


class UserService:
    """Initialise the business logic
    for user service operations."""
    def __init__(
            self,
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
                raise UserCreateError(
                    "Failed to create User."
                )
            return created_user

        except Exception:
            logger.error(
                "Error while creating user",
                exc_info=True
            )
            raise UserCreateError(
                "Error while creating user."
            )


    def get_user(self, user_id: int) \
            -> Optional[UserPublic]:
        """Get a user by id."""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                logger.warning(
                    f"User {user_id} not found"
                )
                raise UserNotFoundError(
                    f"User with user ID {user_id} "
                    f"not found."
                )
            logger.debug(f"Retrieved User {user_id}")
            return user

        except UserNotFoundError:
            raise

        except Exception:
            logger.error(
                f"Error while retrieving "
                f"User {user_id}",
                exc_info=True
            )
            raise UserServiceError(
                "Error while retrieving user."
            )


    def list_users(
            self,
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
            logger.debug(
                f"Listed {len(users)} users "
                f"with filter name={filters.name}"
            )
            return users
        except Exception:
            raise UserServiceError("Error while listing users.")


    def update_user(
            self,
            user_id: int,
            user: UserUpdate) \
            -> Optional[UserPublic]:
        """Make changes by a user."""
        try:
            existing = self.user_repo.get_by_id(user_id)
            if not existing:
                logger.warning(
                    f"Attempted update on "
                    f"non-existing User {user_id}"
                )
                raise UserNotFoundError(
                    f"User with ID {user_id} "
                    f"not found"
                )

            updated_user =self.user_repo.update(user_id, user)
            if not updated_user:
                logger.error(
                    "Error while updating user",
                    exc_info=True
                )
                raise UserUpdateError(
                    "Error while updating user."
                )
            logger.info(f"Updated User {user_id}")
            return updated_user

        except (UserNotFoundError, UserUpdateError):
            raise

        except Exception:
            logger.error(
                f"Error while updating "
                f"user {user_id}",
                exc_info=True
            )
            raise UserUpdateError(
                "Error while updating user."
            )


    def delete_user(self, user_id: int) -> Optional[UserPublic]:
        """Delete a user and the belonging campaign,
        classes, dice sets and logs."""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                logger.warning(
                    f"Attempted delete a "
                    f"non-existing user {user_id}. "
                )
                raise UserNotFoundError(
                    f"User with ID {user_id} "
                    f"not found."
                )

            # Delete dice logs
            for log in (self.dicelog_repo
                    .list_by_user(user_id)):
                self.dicelog_repo.delete(log.id)
                logger.info(
                    f"Deleted DiceLog {log.id} "
                    f"for User {user_id}"
                )

            # Delete dice sets
            for diceset in (self.diceset_repo
                    .list_by_user(user_id)):
                self.diceset_repo.delete(diceset.id)
                logger.info(
                    f"Deleted DiceSet {diceset.id} "
                    f"for User {user_id}"
                )

            # Delete classes
            for dnd_class in (self.class_repo
                    .list_by_user(user_id)):
                self.class_repo.delete(dnd_class.id)
                logger.info(
                    f"Deleted DnDClass {dnd_class.id} "
                    f"for User {user_id}"
                )

            # Delete campaigns
            for campaign in (self.campaign_repo
                    .list_by_user(user_id)):
                self.campaign_repo.delete(campaign.id)
                logger.info(
                    f"Deleted Campaign {campaign.id} "
                    f"for User {user_id}"
                )

            # Finally delete user
            deleted_user = self.user_repo.delete(user_id)
            if not deleted_user:
                logger.error(
                    f"Failed to delete User {user_id}"
                )
                raise UserDeleteError(
                    "Failed to delete user."
                )
            logger.info(
                f"Deleted User {user_id} "
                f"- {deleted_user.user_name}"
            )
            return deleted_user

        except Exception:
            logger.error(
                f"Error while deleting "
                f"user {user_id}",
                exc_info=True
            )
            raise UserDeleteError(
                f"Error while deleting user {user_id}."
            )
