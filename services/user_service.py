"""
user_service.py

Business logic for user.
"""
from fastapi import HTTPException
from typing import List, Optional
from models.schemas.user_schema import *
from repositories.user_repository import UserRepository
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository



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


    def create_user(self, user: UserCreate) -> UserPublic:
        """Create a new user."""
        return self.user_repo.add(user)


    def get_user(self, user_id: int) -> Optional[UserPublic]:
        """Get a user by id."""
        return self.user_repo.get_by_id(user_id)


    def list_users(self,
                   offset: int = 0,
                   limit: int = 100
                   ) -> List[UserPublic]:
        """Get a list of all users."""
        return self.user_repo.list_all(offset=offset,
                                       limit=limit)


    def update_user(self,
                    user_id: int,
                    user: UserUpdate) -> Optional[UserPublic]:
        """Make changes by a user."""
        return self.user_repo.update(user_id, user)


    def delete_user(self, user_id: int) -> bool:
        """Delete a user and the belonging campaign,
        classes, dice sets and logs."""

        # Delete dice logs
        logs = self.dicelog_repo.list_by_user(user_id)
        for log in logs:
            self.dicelog_repo.delete(log.id)

        # Delete dice sets
        dicesets = self.diceset_repo.list_by_user(user_id)
        for diceset in dicesets:
            self.diceset_repo.delete(diceset.id)

        # Delete classes
        dnd_classes = self.class_repo.list_by_user(user_id)
        for dnd_class in dnd_classes:
            self.class_repo.delete(dnd_class.id)

        # Delete campaigns
        campaigns = self.campaign_repo.list_by_user(user_id)
        for campaign in campaigns:
            self.campaign_repo.delete(campaign.id)

        # Finally delete user
        return self.user_repo.delete(user_id)
