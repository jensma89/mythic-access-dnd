"""
class_service.py

Business logic for classes.
"""
from fastapi import Query
from typing import List, Optional, Annotated
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository



class ClassService:
    """Initialise the bussines logic
    for class service operations."""
    def __init__(self, repository: ClassRepository):
        self.repo = repository


    def create_class(self, dnd_class: ClassCreate) -> ClassPublic:
        """Create a new class."""
        return self.repo.add(dnd_class)


    def get_class(self, class_id: int) -> Optional[ClassPublic]:
        """Get the class by id."""
        return self.repo.get_by_id(class_id)


    def list_classes(self,
                     offset: Annotated[int, Query(ge=0)] = 0,
                     limit: Annotated[int, Query(le=100)] = 100
                     ) -> Optional[ClassPublic]:
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
