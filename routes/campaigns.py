"""
campaigns.py

The API routes for campaigns.
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import SessionDep
from models.schemas.campaign_schema import *
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from services.campaign_service import CampaignService


router = APIRouter(tags=["campaigns"])


async def get_campaign_service(session: SessionDep) -> CampaignService:
    """Factory to get the campaign service."""
    repo = SqlAlchemyCampaignRepository(session)
    return CampaignService(repo)


@router.get("/campaigns/{campaign_id}", response_model=CampaignPublic)
async def read_campaign(campaign_id: int,
                        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to get a single campaign."""
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404,
                            detail="Campaign not found.")
    return campaign


@router.get("/campaigns/",
            response_model=List[CampaignPublic])
async def read_campaigns(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to get all campaigns."""
    return service.list_campaigns(offset, limit)


@router.post("/campaigns/",
             response_model=CampaignPublic)
async def create_campaign(
        campaign: CampaignCreate,
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to create a new campaign."""
    return service.create_campaign(campaign)


@router.patch("/campaigns/{campaign_id}",
            response_model=CampaignPublic)
async def update_campaign(
        campaign_id: int,
        campaign: CampaignUpdate,
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to change campaign data."""
    updated = service.update_campaign(campaign_id, campaign)
    if not updated:
        raise HTTPException(status_code=404,
                            detail="Campaign not found")
    return updated


@router.delete("/campaigns/{campaign_id}",
               response_model=CampaignPublic)
async def delete_campaign(
        campaign_id: int,
        service: CampaignService = Depends(get_campaign_service)):
    """Endpoint to remove a campaign."""
    deleted = service.delete_campaign(campaign_id)
    if not deleted:
        raise HTTPException(status_code=404,
                            detail="Campaign not found")
    return deleted
