"""
class_repository.py

Defined methods for class management.
"""
from fastapi import Query
from abc import ABC, abstractmethod
from typing import Annotated, List, Optional
from models.schemas.class_schema import *



class ClassRepository(ABC):
    """This class defines the management methods for classes."""

    @abstractmethod
    def get_by_id(self, class_id: int) -> Optional[ClassPublic]:
        """Method to get class by ID."""
        pass


    @abstractmethod
    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[ClassPublic]:
        """Show all classes method."""
        pass


    @abstractmethod
    def add(self, dnd_class: ClassCreate) -> ClassPublic:
        """Add new class method."""
        pass


    @abstractmethod
    def update(self,
               class_id: int,
               dnd_class: ClassUpdate) -> Optional[ClasPublic]:
        """Model to change data."""
        pass


    @abstractmethod
    def delete(self, class_id: int) -> bool:
        """Delete class method."""
        pass
