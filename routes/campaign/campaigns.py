"""
campaigns.py

The API routes for campaigns.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from dependencies import CampaignQueryParams, Pagination, SessionDep
from models.schemas.campaign_schema import *
from services.campaign.campaign_service import CampaignService
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from services.campaign.campaign_service_exceptions import (
    CampaignNotFoundError,
    CampaignServiceError
)
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter

router = APIRouter(tags=["campaigns"])
logger = logging.getLogger(__name__)


def get_campaign_service(session: SessionDep) \
        -> CampaignService:
    """Factory to get the campaign, dnd_class,
    dice set and dice log service."""
    campaign_repo = SqlAlchemyCampaignRepository(session)
    class_repo = SqlAlchemyClassRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)
    dicelog_repo = SqlAlchemyDiceLogRepository(session)
    return CampaignService(
        campaign_repo,
        class_repo,
        diceset_repo,
        dicelog_repo
    )


@router.get("/campaigns/{campaign_id}",
            response_model=CampaignPublic)
@limiter.limit("10/minute")
def read_campaign(
        request: Request,
        campaign_id: int = Path(
            ...,
            description="The ID of the campaign to retrieve"
        ),
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)
):
    """Endpoint to get a single campaign (owner only)."""
    logger.info(f"GET campaign {campaign_id} "
                f"by user {current_user.id}")
    try:
        campaign = service.get_campaign(campaign_id)
    except CampaignNotFoundError:
        logger.warning(
            f"Campaign {campaign_id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="Campaign not found."
        )
    except CampaignServiceError:
        logger.exception(
            f"Error while retrieving "
            f"campaign {campaign_id}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error while retrieving campaign."
        )
    if campaign.created_by != current_user.id:
        logger.warning(
            f"User {current_user.id} tried to access "
            f"campaign {campaign_id} not owned by them"
        )
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )
    return campaign


@router.get("/campaigns/",
            response_model=List[CampaignPublic])
@limiter.limit("10/minute")
def read_campaigns(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        filters: CampaignQueryParams = Depends(),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to get all campaigns owned by the current user."""
    logger.info(f"GET campaigns list by user {current_user.id}")
    filters.user_id = current_user.id
    return service.list_campaigns(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters
    )


@router.post("/campaigns/",
             response_model=CampaignPublic)
@limiter.limit("3/minute")
def create_campaign(
        request: Request,
        campaign: CampaignCreateInput,
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to create a new campaign."""
    logger.info(f"POST create campaign by user {current_user.id}")

    # Set current user as owner
    campaign = CampaignCreate(**campaign.model_dump())
    campaign.set_user(current_user.id)
    created = service.create_campaign(campaign)
    logger.info(f"Campaign {created.id} created by user {current_user.id}")
    return created


@router.patch("/campaigns/{campaign_id}",
            response_model=CampaignPublic)
@limiter.limit("5/minute")
def update_campaign(
        request: Request,
        campaign: CampaignUpdate,
        campaign_id: int = Path(..., description="The ID of the campaign to update."),
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to change campaign data."""

    # Check if the user is the owner
    existing_campaign = service.get_campaign(campaign_id)
    if existing_campaign.created_by != current_user.id:
        logger.warning(f"User {current_user.id} tried to update campaign {campaign_id} not owned by them")
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    logger.info(f"PATCH update campaign {campaign_id} by user {current_user.id}")
    updated = service.update_campaign(campaign_id, campaign)
    if not updated:
        logger.warning(f"Campaign {campaign_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Campaign not found")
    return updated


@router.delete("/campaigns/{campaign_id}",
               response_model=CampaignPublic)
@limiter.limit("5/minute")
def delete_campaign(
        request: Request,
        campaign_id: int = Path(..., description="The ID of the campaign to delete."),
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to remove a campaign."""

    # Check if the user is the owner
    existing_campaign = service.get_campaign(campaign_id)
    if existing_campaign.created_by != current_user.id:
        logger.warning(f"User {current_user.id} tried to delete campaign {campaign_id} not owned by them")
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    logger.info(f"DELETE campaign {campaign_id} by user {current_user.id}")
    deleted = service.delete_campaign(campaign_id)
    if not deleted:
        logger.warning(f"Campaign {campaign_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Campaign not found")
    return deleted
