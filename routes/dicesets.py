"""
dicesets.py

API endpoints for handling dice sets.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from dependencies import Pagination, SessionDep
from models.schemas.diceset_schema import *
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from services.diceset_service import DiceSetService
from auth.auth import get_current_user
from models.db_models.table_models import User



router = APIRouter(tags=["dicesets"])


def get_diceset_service(session: SessionDep) \
        -> DiceSetService:
    """Factory to get the dice, dice set and dice log service."""
    dice_repo = SqlAlchemyDiceRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)
    dicelog_repo = SqlAlchemyDiceLogRepository(session)
    return DiceSetService(dice_repo,
                          diceset_repo,
                          dicelog_repo)


@router.get("/dicesets/{diceset_id}",
            response_model=DiceSetPublic)
def read_diceset(
        diceset_id: int = Path(..., description="The ID of dice set to retrieve."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to get a single dice set."""
    diceset = service.get_diceset(diceset_id)
    if not diceset:
        raise HTTPException(
            status_code=404,
            detail="Diceset not found.")
    return diceset


@router.get("/dicesets/",
            response_model=List[DiceSetPublic])
def read_dicesets(
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to list all dice sets."""
    return service.list_dicesets(
        offset=pagination.offset,
        limit=pagination.limit)


@router.post("/dicesets/",
             response_model=DiceSetPublic)
def create_diceset(
        diceset: DiceSetCreate,
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to create a new dice set."""
    return service.create_diceset(diceset)


@router.patch("/dicesets/{diceset_id}",
              response_model=DiceSetPublic)
def update_diceset(
        diceset: DiceSetUpdate,
        diceset_id: int = Path(..., description="The ID of dice set to update."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to change data from a dice set."""
    updated = service.update_diceset(diceset_id, diceset)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Dice set not found.")
    return updated


@router.delete("/dicesets/{diceset_id}",
               response_model=DiceSetPublic)
def delete_diceset(
        diceset_id: int = Path(..., description="The ID of dice set to delete."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to delete a dice set by ID."""
    deleted = service.delete_diceset(diceset_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dice set not found.")
    return deleted


@router.post("/dicesets/{diceset_id}/roll",
             response_model=DiceSetRollResult)
def roll_diceset(
        diceset_id: int = Path(..., description="The ID of the dice set to roll"),
        user_id: int = Query(..., description="User ID"),
        campaign_id: int = Query(..., description="Campaign ID"),
        class_id: int = Query(..., description="Class ID"),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to roll a specific dice set
    and get the individual results and the total sum."""
    result = service.roll_diceset(
        user_id,
        campaign_id,
        class_id,
        diceset_id
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Dice set not found.")
    return result
