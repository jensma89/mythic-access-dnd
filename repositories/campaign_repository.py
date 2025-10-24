"""
campaign_repository.py

Defined methods for campaign management.
"""
from fastapi import Query
from abc import ABC, abstractmethod
from typing import Annotated, List, Optional
from models.schemas.campaign_schema import *



class CampaignRepository(ABC):
    """This class defines the management methods for campaigns."""

    @abstractmethod
    def get_by_id(self, campaign_id: int) -> Optional[CampaignPublic]:
        """Method to get campaign by ID."""
        pass


    @abstractmethod
    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[CampaignPublic]:
        """Show all campaigns method."""
        pass


    @abstractmethod
    def add(self, campaign: CampaignCreate) -> CampaignPublic:
        """Create a new campaign method."""
        pass


    @abstractmethod
    def update(self,
               campaign_id: int,
               campaign: CampaignUpdate
               ) -> Optional[CampaignPublic]:
        """Method to make changes by campaigns."""
        pass


    @abstractmethod
    def delete(self, campaign_id: int) -> bool:
        """Method to remove a campaign."""
        pass


    @abstractmethod
    def list_by_user(self, user_id: int) -> List[CampaignPublic]:
        """List all campaigns belonging to a specific user."""
        pass


    @abstractmethod
    def list_by_campaign(self, campaign_id: int) -> List[CampaignPublic]:
        """Optional for nested operations."""
        pass
