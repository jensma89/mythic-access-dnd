"""
campaign_service.py

Business logic for campaign.
"""
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from dependencies import CampaignQueryParams
from models.schemas.campaign_schema import *
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository
import logging



logger = logging.getLogger(__name__)


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
        logger.debug("CampaignService initialized")


    def create_campaign(
            self,
            campaign: CampaignCreate) \
            -> CampaignPublic:
        """Create a new campaign."""
        try:
            created = self.campaign_repo.add(campaign)
            if not created:
                logger.warning("Campaign creation failed in repository")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create campaign."
                )
            logger.info(f"Created Campaign {created.id} - {created.title}")
            return created
        except SQLAlchemyError:
            logger.exception("Database error while creating Campaign", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while creating campaign."
            )


    def get_campaign(
            self,
            campaign_id: int) \
            -> Optional[CampaignPublic]:
        """Get a campaign by ID."""
        try:
            campaign = self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                logger.warning(f"Campaign {campaign_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Campaign with ID {campaign_id} not found."
                )

            logger.info(f"Retrieved Campaign {campaign_id} - {campaign.title}")
            return campaign

        except SQLAlchemyError:
            logger.exception(f"Database error while retrieving Campaign {campaign_id}", exc_info=True)
            raise HTTPException(status_code=500, detail="Database error while retrieving campaign.")


    def list_campaigns(
            self,
            filters: CampaignQueryParams,
            offset: int = 0,
            limit: int = 100,) \
            -> List[CampaignPublic]:
        """Get a list of all campaigns."""
        try:
            campaigns = self.campaign_repo.list_all(
                user_id=filters.user_id,
                name=filters.name,
                offset=offset,
                limit=limit
            )
            logger.info(f"Listed {len(campaigns)} Campaigns (offset={offset}, limit={limit})")
            return campaigns

        except SQLAlchemyError:
            logger.exception("Database error while listing Campaigns", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while listing campaigns."
            )


    def update_campaign(
            self,
            campaign_id: int,
            campaign: CampaignUpdate) \
            -> Optional[CampaignPublic]:
        """Update a campaign with new data."""
        try:
            updated = self.campaign_repo.update(
                campaign_id,
                campaign)
            if not updated:
                logger.warning(f"Campaign {campaign_id} not found for update")
                raise HTTPException(
                    status_code=404,
                    detail=f"Campaign with ID {campaign_id} "
                           f"not found."
                )
            logger.info(f"Updated Campaign {campaign_id} - {updated.title}")
            return updated

        except SQLAlchemyError:
            logger.exception(f"Database error while updating Campaign {campaign_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while updating campaign."
            )


    def delete_campaign(
            self,
            campaign_id: int):
        """Remove a campaign and the belonging entries:
        classes, dice sets and dice logs."""
        try:
            campaign = self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                logger.warning(f"Campaign {campaign_id} not found for deletion")
                raise HTTPException(
                    status_code=404,
                    detail=f"Campaign with ID {campaign_id} "
                           f"not found."
                )

            # Delete dice logs
            for log in (self.dicelog_repo
                    .list_by_campaign(campaign_id)):
                self.dicelog_repo.delete(log.id)

            # Delete dice sets
            for diceset in (self.diceset_repo
                    .list_by_campaign(campaign_id)):
                self.diceset_repo.delete(diceset.id)

            # Delete classes
            for dnd_class in (self.class_repo
                    .list_by_campaign(campaign_id)):
                self.class_repo.delete(dnd_class.id)

            # Finally delete campaign
            deleted_campaign = (self.campaign_repo
                              .delete(campaign_id))
            if not deleted_campaign:
                logger.warning(f"Failed to delete Campaign {campaign_id}")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete campaign."
                )
            logger.info(f"Deleted Campaign {campaign_id} - {deleted_campaign}")
            return deleted_campaign

        except SQLAlchemyError:
            logger.exception(f"Database error while deleting Campaign {campaign_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while deleting campaign."
            )
        except Exception:
            logger.exception(f"Unexpected error while deleting Campaign {campaign_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error "
                       f"while deleting campaign.")
