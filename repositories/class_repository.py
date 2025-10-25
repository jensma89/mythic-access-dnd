"""
class_repository.py

Defined methods for class management.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas.class_schema import *



class ClassRepository(ABC):
    """This class defines the management methods for classes."""

    @abstractmethod
    def get_by_id(self, class_id: int) \
            -> Optional[ClassPublic]:
        """Method to get class by ID."""
        pass


    @abstractmethod
    def list_all(self,
                 offset: int = 0,
                 limit: int = 100
                 ) -> List[ClassPublic]:
        """Show all classes method."""
        pass


    @abstractmethod
    def add(self, dnd_class: ClassCreate) \
            -> ClassPublic:
        """Add new class method."""
        pass


    @abstractmethod
    def update(self,
               class_id: int,
               dnd_class: ClassUpdate) \
            -> Optional[ClassPublic]:
        """Model to change data."""
        pass


    @abstractmethod
    def delete(self, class_id: int) -> bool:
        """Delete class method."""
        pass


    @abstractmethod
    def get_by_campaign_id(self, campaign_id: int) \
            -> List[ClassPublic]:
        """Get all classes belonging to a campaign."""
        pass


    @abstractmethod
    def list_by_user(self, user_id: int) \
            -> List[ClassPublic]:
        """List all classes belonging to a specific user."""
        pass


    @abstractmethod
    def list_by_campaign(self, campaign_id: int) \
            -> List[ClassPublic]:
        """List all classes belonging to a specific campaign."""
        pass


    @abstractmethod
    def list_by_class(self, class_id: int) \
            -> List[ClassPublic]:
        """Optional for nested operations."""
        pass
