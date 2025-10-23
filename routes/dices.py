"""
dices.py

API endpoints for dices.
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import SessionDep
from models.schemas.dice_schema import *
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from services.dice_service import DiceService


router = APIRouter(tags=["dices"])



async def get_dice_service(session: SessionDep) -> DiceService:
    """Factory to get the dice service."""
    dice_repo = SqlAlchemyDiceRepository(session)
    log_repo = SqlAlchemyDiceLogRepository(session)
    return DiceService(dice_repo, log_repo)


@router.get("/dices/{dice_id}", response_model=DicePublic)
async def read_dice(dice_id: int,
                    service: DiceService = Depends(get_dice_service)):
    """Endpoint to get a single dice."""
    dice = service.get_dice(dice_id)
    if not dice:
        raise HTTPException(status_code=404,
                            detail="Dice not found.")
    return dice


@router.get("/dices/", response_model=List[DicePublic])
async def read_dices(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to list all dices."""
    return service.list_dices(offset, limit)


@router.post("/dices/", response_model=DicePublic)
async def create_dice(
        dice: DiceCreate,
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to create a new dice."""
    return service.create_dice(dice)


@router.patch("/dices/{dice_id}", response_model=DicePublic)
async def update_dice(
        dice_id: int,
        dice: DiceUpdate,
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to change data from a dice."""
    updated = service.update_dice(dice_id, dice)
    if not updated:
        raise HTTPException(status_code=404,
                            detail="Dice not found.")
    return updated


@router.delete("/dices/{dice_id}", response_model=DicePublic)
async def delete_dice(
        dice_id: int,
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to delete a dice."""
    deleted = service.delete_dice(dice_id)
    if not deleted:
        raise HTTPException(status_code=404,
                            detail="Dice not found.")
    return deleted


@router.post("/dices/{dice_id}/roll", response_model=DiceRollResult)
async def roll_dice(
        dice_id: int,
        service: DiceService = Depends(get_dice_service)):
    """Endpoint to roll a specific dice and get the result (random)."""
    roll = service.roll_dice(dice_id)
    return roll
