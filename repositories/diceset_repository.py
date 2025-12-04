"""
diceset_repository

Defined methods for dice set management.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas.diceset_schema import *



class DiceSetRepository(ABC):
    """This dnd_class defines the management methods for dice sets."""

    @abstractmethod
    def get_by_id(self, diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Get a dice set by ID."""
        pass


    @abstractmethod
    def list_all(self,
                 offset: int = 0,
                 limit: int = 100
                 ) -> List[DiceSetPublic]:
        """Show all dice sets method."""
        pass


    @abstractmethod
    def add(self, diceset: DiceSetCreate) \
            -> Optional[DiceSetPublic]:
        """Method to add a new dice set."""
        pass


    @abstractmethod
    def update(self,
               diceset_id: int,
               diceset: DiceSetUpdate) \
            -> Optional[DiceSetPublic]:
        """Method to change the data from a dice set."""
        pass


    @abstractmethod
    def delete(self, diceset_id: int):
        """Method to remove a dice set."""
        pass


    @abstractmethod
    def get_by_class_id(self, class_id: int) \
            -> List[DiceSetPublic]:
        """Get all dice sets belonging to a dnd_class."""
        pass


    @abstractmethod
    def list_by_user(self, user_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific user."""
        pass


    @abstractmethod
    def list_by_campaign(self, campaign_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific campaign."""
        pass


    @abstractmethod
    def list_by_class(self, class_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific DnD dnd_class."""
        pass
