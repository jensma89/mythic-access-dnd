"""
dice_repository.py

Defined methods for dice management.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas.dice_schema import *



class DiceRepository(ABC):
    """This class defines the management methods for dices."""

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
    def delete(self, dice_id: int) -> bool:
        """Method to remove a dice."""
        pass


    @abstractmethod
    def get_by_class_id(self, class_id: int) \
            -> List[DicePublic]:
        """Get all dices belonging to a class."""
        pass
