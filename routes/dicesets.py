"""
dicesets.py

API endpoints for handling dice sets.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from dependencies import Pagination, SessionDep
from models.schemas.diceset_schema import *
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from services.diceset_service import DiceSetService



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
        diceset_id: int,
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
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to create a new dice set."""
    return service.create_diceset(diceset)


@router.patch("/dicesets/{diceset_id}",
              response_model=DiceSetPublic)
def update_diceset(
        diceset_id: int,
        diceset: DiceSetUpdate,
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to change data from a dice set."""
    updated = service.update_diceset(diceset_id, diceset)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Dice set not found.")
    return updated


@router.post("/dicesets/{diceset_id}/roll",
             response_model=DiceSetRollResult)
def roll_diceset(
        user_id: int,    # remove after auth implementation?
        campaign_id: int,
        class_id: int,
        diceset_id: int,
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


@router.delete("/dicesets/{diceset_id}",
               response_model=DiceSetPublic)
def delete_diceset(
        diceset_id: int,
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to delete a dice set by ID."""
    deleted = service.delete_diceset(diceset_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dice set not found.")
    return deleted
