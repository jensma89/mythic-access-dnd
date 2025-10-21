"""
diceset_repository

Defined methods for dice set management.
"""
from fastapi import Query
from abc import ABC, abstractmethod
from typing import Annotated, List, Optional
from models.schemas.diceset_schema import *



class DiceSetRepository(ABC):
    """This class defines the management methods for dice sets."""

    @abstractmethod
    def get_by_id(self, diceset_id: int) -> Optional[DiceSetPublic]:
        """Get a dice set by ID."""
        pass


    @abstractmethod
    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[DiceSetPublic]:
        """Show all dice sets method."""
        pass


    @abstractmethod
    def add(self, diceset: DiceSetCreate) -> Optional[DiceSetPublic]:
        """Method to add a new dice set."""
        pass


    @abstractmethod
    def update(self,
               diceset_id: int,
               diceset: DiceSetUpdate) -> Optional[DiceSetPublic]:
        """Method to change the data from a dice set."""
        pass


    @abstractmethod
    def delete(self, diceset_id: int) -> bool:
        """Method to remove a dice set."""
        pass


    @abstractmethod
    def get_by_class_id(self, class_id: int) -> List[DiceSetPublic]:
        """Get all dice sets belonging to a class."""
        pass
