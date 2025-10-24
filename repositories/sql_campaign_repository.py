"""
sql_campaign_repository.py

Concrete implementation for sqlalchemy, campaign management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import Campaign
from models.schemas.campaign_schema import *
from repositories.campaign_repository import CampaignRepository



class SqlAlchemyCampaignRepository(CampaignRepository):
    """This class implement
    the campaign handling methods with sqlalchemy."""
    def __init__(self, session: Session):
        self.session = session


    def list_by_user(self, user_id: int) -> List[CampaignPublic]:
        """List all campaigns belonging to a specific user."""
        campaigns = self.session.exec(
            select(Campaign)
            .where(Campaign.user_id == user_id)
        ).all()
        return [CampaignPublic.model_validate(c) for c in campaigns]


    def list_by_campaign(self, campaign_id: int) -> List[CampaignPublic]:
        """Return a single campaign as list for uniformity."""
        campaign = self.session.exec(
            select(Campaign)
            .where(Campaign.id == campaign_id)
        ).all()
        return [CampaignPublic.model_validate(c) for c in campaign]


    def get_by_id(self, campaign_id: int) -> Optional[CampaignPublic]:
        """Method to get campaign by ID."""
        db_campaign = self.session.get(Campaign, campaign_id)
        if db_campaign:
            return CampaignPublic.model_validate(db_campaign)
        return None


    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[CampaignPublic]:
        """Method to show all campaigns."""
        campaigns = self.session.exec(
            select(Campaign)
            .offset(offset)
            .limit(limit)).all()
        return [CampaignPublic.model_validate(c) for c in campaigns]


    def add(self, campaign: CampaignCreate) -> CampaignPublic:
        """Method to add a new campaign."""
        db_campaign = Campaign(**campaign.model_dump())
        self.session.add(db_campaign)
        self.session.commit()
        self.session.refresh(db_campaign)
        return CampaignPublic.model_validate(db_campaign)


    def update(self,
               campaign_id: int,
               campaign: CampaignUpdate) -> Optional[CampaignPublic]:
        """Method to change the data of campaign."""
        db_campaign = self.session.get(Campaign, campaign_id)
        if not db_campaign:
            return None
        for key, value in campaign.model_dump(exclude_unset=True).items():
            setattr(db_campaign, key, value)
        self.session.add(db_campaign)
        self.session.commit()
        self.session.refresh(db_campaign)
        return CampaignPublic.model_validate(db_campaign)


    def delete(self, campaign_id: int) -> Optional[CampaignPublic]:
        """Method to remove a campaign."""
        db_campaign = self.session.get(Campaign, campaign_id)
        if not db_campaign:
            return None
        self.session.delete(db_campaign)
        self.session.commit()
        return CampaignPublic.model_validate(db_campaign)
