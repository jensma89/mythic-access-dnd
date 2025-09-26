"""
campaign_service.py

Business logic for campaign.
"""
from fastapi import Query
from typing import List, Optional, Annotated
from models.schemas.campaign_schema import *
from repositories.campaign_repository import CampaignRepository



class CampaignService:
    """Initialise the bussines logic
    for campaign service operations."""
    def __init__(self, repository: CampaignRepository):
        self.repo = repository


    def create_campaign(self, campaign: CampaignCreate) -> CampaignPublic:
        """Create a new campaign."""
        return self.repo.add(campaign)


    def get_campaign(self, campaign_id: int) -> Optional[CampaignPublic]:
        """Get a campaign by ID."""
        return self.repo.get_by_id(campaign_id)


    def list_campaigns(self,
                       offset: Annotated[int, Query(ge=0)] = 0,
                       limit: Annotated[int, Query(le=100)] = 100
                       ) -> List[CampaignPublic]:
        """Get a list of all campaigns."""
        return self.repo.list_all(offset, limit)


    def update_campaign(self,
                        campaign_id: int,
                        campaign: CampaignUpdate
                        ) -> Optional[CampaignPublic]:
        """Update a campaign with new data."""
        return self.repo.update(campaign_id, campaign)


    def delete_campaign(self, campaign_id: int) -> bool:
        """Remove a campaign."""
        return self.repo.delete(campaign_id)
