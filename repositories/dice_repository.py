"""
dice_repository.py

Defined methods for dice management.
"""
from abc import ABC, abstractmethod
from models.schemas.dice_schema import *
from typing import List, Optional



class DiceRepository(ABC):
    """This dnd_class defines the management methods for dices."""

    @abstractmethod
    def get_by_id(self, dice_id: int) \
            -> Optional[DicePublic]:
        """Method to get dice by id"""
        pass


    @abstractmethod
    def list_all(self,
                 offset: int = 0,
                 limit: int = 100
                 ) -> List[DicePublic]:
        """Show all dices method."""
        pass


    @abstractmethod
    def add(self, dice: DiceCreate) \
            -> Optional[DicePublic]:
        """Method to add a new dice."""
        pass


    @abstractmethod
    def update(self,
               dice_id: int,
               dice: DiceUpdate) \
            -> Optional[DicePublic]:
        """Method to change data from a dice"""
        pass


    @abstractmethod
    def delete(self, dice_id: int):
        """Method to remove a dice."""
        pass


    @abstractmethod
    def get_by_class_id(self, class_id: int) \
            -> List[DicePublic]:
        """Get all dices belonging to a dnd_class."""
        pass
