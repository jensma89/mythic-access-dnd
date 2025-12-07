"""
campaign_service.py

Business logic for campaign.
"""
import logging
from typing import List

from dependencies import CampaignQueryParams
from models.schemas.campaign_schema import *
from repositories.campaign_repository import CampaignRepository
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository
from services.campaign.campaign_service_exceptions import *



logger = logging.getLogger(__name__)


class CampaignService:
    """Initialise the bussines logic
    for campaign service operations."""
    def __init__(
            self,
            campaign_repo: CampaignRepository,
            class_repo: ClassRepository,
            diceset_repo: DiceSetRepository,
            dicelog_repo: DiceLogRepository
    ):
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
                logger.warning(
                    "Campaign creation failed in repository"
                )
                raise CampaignCreateError(
                    "Failed to create campaign."
                )
            logger.info(
                f"Created Campaign {created.id} "
                f"- {created.title}"
            )
            return created
        except Exception:
            logger.exception(
                "Error while creating Campaign",
                exc_info=True
            )
            raise CampaignCreateError(
                "Error while creating campaign."
            )


    def get_campaign(
            self,
            campaign_id: int) \
            -> Optional[CampaignPublic]:
        """Get a campaign by ID."""
        try:
            campaign = self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                logger.warning(
                    f"Campaign {campaign_id} "
                    f"not found"
                )
                raise CampaignNotFoundError(
                    f"Campaign with ID {campaign_id} "
                    f"not found."
                )
            logger.info(
                f"Retrieved Campaign {campaign_id} "
                f"- {campaign.title}"
            )
            return campaign

        except CampaignNotFoundError:
            raise
        except Exception:
            logger.exception(
                f"Error while retrieving "
                f"Campaign {campaign_id}",
                exc_info=True
            )
            raise CampaignServiceError(
                "Error while retrieving campaign."
            )


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
            logger.info(
                f"Listed {len(campaigns)} Campaigns "
                f"(offset={offset}, "
                f"limit={limit})"
            )
            return campaigns

        except Exception:
            logger.exception(
                "Error while "
                "listing Campaigns",
                exc_info=True
            )
            raise CampaignServiceError(
                "Error while listing campaigns."
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
                logger.warning(
                    f"Campaign {campaign_id} "
                    f"not found for update"
                )
                raise CampaignNotFoundError(
                    f"Campaign with ID {campaign_id} "
                    f"not found."
                )
            logger.info(
                f"Updated Campaign {campaign_id} "
                f"- {updated.title}"
            )
            return updated

        except Exception:
            logger.exception(
                f"Error while updating "
                f"Campaign {campaign_id}",
                exc_info=True
            )
            raise CampaignServiceError(
                "Error while updating campaign."
            )


    def delete_campaign(
            self,
            campaign_id: int):
        """Remove a campaign and the belonging entries:
        classes, dice sets and dice logs."""
        try:
            campaign = self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                logger.warning(
                    f"Campaign {campaign_id} "
                    f"not found for deletion"
                )
                raise CampaignNotFoundError(
                    f"Campaign with ID {campaign_id} "
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
                logger.warning(
                    f"Failed to delete "
                    f"Campaign {campaign_id}"
                )
                raise CampaignDeleteError(
                    "Failed to delete campaign."
                )
            logger.info(
                f"Deleted Campaign {campaign_id} "
                f"- {deleted_campaign}"
            )
            return deleted_campaign


        except CampaignServiceError:
            raise

        except Exception:
            logger.exception(
                "Error while deleting campaign"
            )
            raise CampaignServiceError(
                "Error while deleting campaign."
            )
