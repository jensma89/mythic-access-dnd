"""
class_service.py

Business logic for classes.
"""
from fastapi import HTTPException
from dependencies import ClassQueryParams
from typing import List, Optional
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository



class ClassService:
    """Business logic
    for class service operations."""

    def __init__(self,
                 class_repo: ClassRepository,
                 diceset_repo: DiceSetRepository,
                 dicelog_repo: DiceLogRepository):
        self.class_repo = class_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo


    def create_class(self, dnd_class: ClassCreate) \
            -> ClassPublic:
        """Create a new class (max. 4 per campaign)."""

        #Get the count of classes for a campaign
        existing_classes = (
            self.class_repo
            .get_by_campaign_id(dnd_class.campaign_id))

        if len(existing_classes) >= 4:
            raise HTTPException(
                status_code=400,
                detail="Campaign already has 4 classes. "
                       "Maximum reached."
            )
        # If limit not reached, create a new class
        return self.class_repo.add(dnd_class)


    def get_class(self, class_id: int) \
            -> Optional[ClassPublic]:
        """Get the class by id."""
        return self.class_repo.get_by_id(class_id)


    def list_classes(self,
                     filters: ClassQueryParams,
                     offset: int = 0,
                     limit: int = 100
                     ) -> List[ClassPublic]:
        """Get a list of all classes."""
        return self.class_repo.list_all(
            campaign_id=filters.campaign_id,
            name=filters.name,
            offset=offset,
            limit=limit)


    def update_class(self,
                     class_id: int,
                     dnd_class: ClassUpdate) \
            -> Optional[ClassPublic]:
        """Make changes by a class."""
        return self.class_repo.update(class_id, dnd_class)


    def delete_class(self, class_id: int) -> bool:
        """Remove a class and the belonging entries:
        dice sets and dice logs."""

        # Delete dice logs
        logs = self.dicelog_repo.list_by_class(class_id)
        for log in logs:
            self.dicelog_repo.delete(log.id)

        # Delete dice sets
        dicesets = self.diceset_repo.list_by_class(class_id)
        for diceset in dicesets:
            set_logs = self.dicelog_repo.list_by_diceset(diceset.id)
            for log in set_logs:
                self.dicelog_repo.delete(log.id)

        # Finally delete campaign
        return self.class_repo.delete(class_id)
