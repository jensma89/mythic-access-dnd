"""
campaigns.py

The API routes for campaigns.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from dependencies import CampaignQueryParams, Pagination, SessionDep
from models.schemas.campaign_schema import *
from services.campaign_service import CampaignService
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter

router = APIRouter(tags=["campaigns"])


def get_campaign_service(session: SessionDep) \
        -> CampaignService:
    """Factory to get the campaign, class,
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
        campaign_id: int = Path(..., description="The ID of the campaign to retrieve"),
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to get a single campaign."""
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found.")
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
    """Endpoint to get all campaigns."""
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
        campaign: CampaignCreate,
        current_user: User = Depends(get_current_user),
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to create a new campaign."""
    return service.create_campaign(campaign)


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
    updated = service.update_campaign(campaign_id, campaign)
    if not updated:
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
    deleted = service.delete_campaign(campaign_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found")
    return deleted
