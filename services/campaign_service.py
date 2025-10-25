"""
campaign_service.py

Business logic for campaign.
"""
from fastapi import HTTPException
from typing import List, Optional
from models.schemas.campaign_schema import *
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository



class CampaignService:
    """Initialise the bussines logic
    for campaign service operations."""
    def __init__(self,
                 campaign_repo: CampaignRepository,
                 class_repo: ClassRepository,
                 diceset_repo: DiceSetRepository,
                 dicelog_repo: DiceLogRepository):
        self.campaign_repo = campaign_repo
        self.class_repo = class_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo


    def create_campaign(self,
                        campaign: CampaignCreate) -> CampaignPublic:
        """Create a new campaign."""
        return self.campaign_repo.add(campaign)


    def get_campaign(self,
                     campaign_id: int) -> Optional[CampaignPublic]:
        """Get a campaign by ID."""
        return self.campaign_repo.get_by_id(campaign_id)


    def list_campaigns(self,
                       offset: int = 0,
                       limit: int = 100
                       ) -> List[CampaignPublic]:
        """Get a list of all campaigns."""
        return self.campaign_repo.list_all(offset=offset,
                                           limit=limit)


    def update_campaign(self,
                        campaign_id: int,
                        campaign: CampaignUpdate
                        ) -> Optional[CampaignPublic]:
        """Update a campaign with new data."""
        return self.campaign_repo.update(campaign_id, campaign)


    def delete_campaign(self, campaign_id: int) -> bool:
        """Remove a campaign and the belonging entries:
        classes, dice sets and dice logs."""

        # Delete dice logs
        logs = self.dicelog_repo.list_by_campaign(campaign_id)
        for log in logs:
            self.dicelog_repo.delete(log.id)

        # Delete dice sets
        dicesets = self.diceset_repo.list_by_campaign(campaign_id)
        for diceset in dicesets:
            self.diceset_repo.delete(diceset.id)

        # Delete classes
        dnd_classes = self.class_repo.list_by_campaign(campaign_id)
        for dnd_class in dnd_classes:
            self.class_repo.delete(dnd_class.id)

        # Finally delete campaign
        return self.campaign_repo.delete(campaign_id)
