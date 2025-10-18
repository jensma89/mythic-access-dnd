"""
class_service.py

Business logic for classes.
"""
from fastapi import HTTPException, Query
from typing import Annotated, List, Optional
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository



class ClassService:
    """Business logic
    for class service operations."""

    def __init__(self, repository: ClassRepository):
        self.repo = repository


    def create_class(self, dnd_class: ClassCreate) -> ClassPublic:
        """Create a new class (max. 4 per campaign)."""

        #Get the count of classes for a campaign
        existing_classes = self.repo.get_by_campaign_id(dnd_class.campaign_id)

        if len(existing_classes) >= 4:
            raise HTTPException(
                status_code=400,
                detail="Campaign already has 4 classes. "
                       "Maximum reached."
            )
        # If limit not reached, create a new class
        return self.repo.add(dnd_class)


    def get_class(self, class_id: int) -> Optional[ClassPublic]:
        """Get the class by id."""
        return self.repo.get_by_id(class_id)


    def list_classes(self,
                     offset: Annotated[int, Query(ge=0)] = 0,
                     limit: Annotated[int, Query(le=100)] = 100
                     ) -> List[ClassPublic]:
        """Get a list of all classes."""
        return self.repo.list_all(offset, limit)


    def update_class(self,
                     class_id: int,
                     dnd_class: ClassUpdate) -> Optional[ClassPublic]:
        """Make changes by a class."""
        return self.repo.update(class_id, dnd_class)


    def delete_class(self, class_id: int) -> bool:
        """Delete a class by ID."""
        return self.repo.delete(class_id)
