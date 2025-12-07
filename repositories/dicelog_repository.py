"""
dicelog_repository.py

Defined methods for dice log management.
"""
from abc import ABC, abstractmethod
from models.schemas.dicelog_schema import *
from typing import List, Optional



class DiceLogRepository(ABC):
    """This dnd_class defines
    the management methods for dice logs."""


    @abstractmethod
    def get_by_id(self, dicelog_id: int) \
            -> Optional[DiceLogPublic]:
        """Get a dice log by ID."""
        pass


    @abstractmethod
    def add(self, log: DiceLogCreate) \
            -> DiceLogPublic:
        """Add a dice log entry."""
        pass


    @abstractmethod
    def delete(self, dicelog_id: int) \
            -> DiceLogPublic:
        """Remove a dice log entry."""
        pass


    @abstractmethod
    def list_logs(self,
                  user_id: int,
                  offset: int = 0,
                  limit: int = 100) \
            -> List[DiceLogPublic]:
        """List all dice logs."""
        pass


    @abstractmethod
    def list_by_user(self, user_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific user."""
        pass


    @abstractmethod
    def list_by_campaign(self, campaign_id: int)\
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific campaign."""
        pass


    @abstractmethod
    def list_by_class(self, class_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific dnd_class."""
        pass


    @abstractmethod
    def list_by_diceset(self, diceset_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific dice set."""
        pass

    @abstractmethod
    def log_roll(self, log: DiceLogCreate) -> DiceLogPublic:
        pass