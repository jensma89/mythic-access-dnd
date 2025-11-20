"""
dices.py

API endpoints for dices.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from dependencies import Pagination, SessionDep
from models.schemas.dice_schema import *
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from services.dice_service import DiceService
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter
import logging


router = APIRouter(tags=["dices"])
logger = logging.getLogger(__name__)



def get_dice_service(session: SessionDep) \
        -> DiceService:
    """Factory to get the dice and dice log service."""
    dice_repo = SqlAlchemyDiceRepository(session)
    log_repo = SqlAlchemyDiceLogRepository(session)
    return DiceService(dice_repo, log_repo)


@router.get("/dices/{dice_id}",
            response_model=DicePublic)
@limiter.limit("10/minute")
def read_dice(
        request: Request,
        dice_id: int = Path(..., description="The dice ID to retrieve."),
        current_user: User = Depends(get_current_user),
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to get a single dice."""
    logger.info(f"GET dice {dice_id} by user {current_user.id}")
    dice = service.get_dice(dice_id)
    if not dice:
        logger.warning(f"Dice {dice_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Dice not found.")
    return dice


@router.get("/dices/",
            response_model=List[DicePublic])
@limiter.limit("10/minute")
def read_dices(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to list all dices."""
    logger.info(f"GET dice list by user {current_user.id}")
    return service.list_dices(
        offset=pagination.offset,
        limit=pagination.limit)


#@router.post("/dices/",
#             response_model=DicePublic)
#def create_dice(
#        dice: DiceCreate,
#        current_user: User = Depends(get_current_user),
#        service: DiceService = Depends(get_dice_service)):
#    """Endpoint to create a new dice."""
#    return service.create_dice(dice)


#@router.patch("/dices/{dice_id}",
#              response_model=DicePublic)
#def update_dice(
#        dice: DiceUpdate,
#        dice_id: int = Path(..., description=""),
#        current_user: User = Depends(get_current_user),
#        service: DiceService = Depends(get_dice_service)):
#    """Endpoint to change data from a dice."""
#    updated = service.update_dice(dice_id, dice)
#    if not updated:
#        raise HTTPException(
#            status_code=404,
#            detail="Dice not found.")
#    return updated


#@router.delete("/dices/{dice_id}",
#               response_model=DicePublic)
#def delete_dice(
#        dice_id: int = Path(..., description=""),
#        current_user: User = Depends(get_current_user),
#        service: DiceService = Depends(get_dice_service)):
#    """Endpoint to delete a dice."""
#    deleted = service.delete_dice(dice_id)
#    if not deleted:
#        raise HTTPException(
#            status_code=404,
#            detail="Dice not found.")
#   return deleted


@router.post("/dices/{dice_id}/roll",
             response_model=DiceRollResult)
@limiter.limit("30/minute")
def roll_dice(
        request: Request,
        dice_id: int = Path(..., description="The ID of the dice to roll."),
        campaign_id: int | None = Query(None, description="Campaign ID."),
        class_id: int | None = Query(None, description="Class ID."),
        current_user: User = Depends(get_current_user),
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to roll a specific dice
    and get the result (random)."""
    logger.info(f"ROLL dice {dice_id} by user {current_user.id}")

    # Check if the user is the owner
    db_dice = service.repo.get_by_id(dice_id)
    if not db_dice:
        logger.warning(f"Dice {dice_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Dice not found"
        )

    roll_result = service.roll_dice(
        dice_id=dice_id,
        user_id=current_user.id,
        campaign_id=campaign_id,
        class_id=class_id
    )
    if not roll_result:
        logger.warning(f"Dice {dice_id} not found for roll")
        raise HTTPException(
            status_code=404,
            detail="Dice not found.")
    return roll_result
