"""
dicesets.py

API endpoints for handling dice sets.
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from dependencies import Pagination, SessionDep
from models.schemas.diceset_schema import *
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from services.diceset.diceset_service import DiceSetService
from services.diceset.diceset_service_exceptions import (
    DiceSetNotFoundError,
    DiceSetCreateError,
    DiceSetServiceError
)
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter
import logging


router = APIRouter(tags=["dicesets"])
logger = logging.getLogger(__name__)


def get_diceset_service(session: SessionDep) -> DiceSetService:
    """Factory to get the dice, dice set and dice log service."""
    dice_repo = SqlAlchemyDiceRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)
    dicelog_repo = SqlAlchemyDiceLogRepository(session)
    return DiceSetService(dice_repo, diceset_repo, dicelog_repo)


@router.get("/dicesets/{diceset_id}", response_model=DiceSetPublic)
@limiter.limit("10/minute")
def read_diceset(
        request: Request,
        diceset_id: int = Path(..., description="The ID of dice set to retrieve."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to get a single dice set."""
    logger.info(f"GET dice set {diceset_id} by user {current_user.id}")
    try:
        diceset = service.get_diceset(diceset_id)
        return diceset

    except DiceSetNotFoundError:
        logger.warning(f"Dice set {diceset_id} not found")
        raise HTTPException(status_code=404, detail="Dice set not found.")
    except DiceSetServiceError:
        logger.error(f"Service error while fetching dice set {diceset_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.get("/dicesets/", response_model=List[DiceSetPublic])
@limiter.limit("10/minute")
def read_dicesets(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to list all dice sets."""
    logger.info(f"GET dice sets list by user {current_user.id}")
    try:
        return service.list_dicesets(
            offset=pagination.offset,
            limit=pagination.limit)

    except DiceSetServiceError:
        logger.error("Service error while listing dice sets")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.post("/dicesets/", response_model=DiceSetPublic)
@limiter.limit("5/minute")
def create_diceset(
        request: Request,
        diceset_input: DiceSetCreateInput,
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to create a new dice set."""
    logger.info(f"CREATE dice set by user {current_user.id}")

    try:
        # Set current user as owner
        diceset = DiceSetCreate(**diceset_input.model_dump())
        diceset.set_user(current_user.id)
        created = service.create_diceset(diceset)
        logger.info(f"Dice set {created.id} created by user {current_user.id}")
        return created

    except DiceSetCreateError:
        logger.warning(f"Failed to create dice set")
        raise HTTPException(status_code=400, detail="Failed to create dice set.")
    except DiceSetNotFoundError:
        logger.warning(f"Dice not found while creating dice set.")
        raise HTTPException(status_code=404, detail="Dice set not found.")
    except DiceSetServiceError:
        logger.error(f"Service error while creating dice set")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.patch("/dicesets/{diceset_id}", response_model=DiceSetPublic)
@limiter.limit("5/minute")
def update_diceset(
        request: Request,
        diceset: DiceSetUpdate,
        diceset_id: int = Path(..., description="The ID of dice set to update."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to change data from a dice set."""
    try:
        # Check if the user is the owner
        existing_diceset = service.get_diceset(diceset_id)
        if existing_diceset.user_id != current_user.id:
            logger.warning(f"User {current_user.id} tried to update dice set {diceset_id} not owned by them")
            raise HTTPException(status_code=403, detail="Not allowed")

        logger.info(f"PATCH update dice set {diceset_id} by user {current_user.id}")
        updated = service.update_diceset(diceset_id, diceset)
        return updated

    except HTTPException:
        raise
    except DiceSetNotFoundError:
        logger.warning(f"Dice set {diceset_id} not found for update")
        raise HTTPException(status_code=404, detail="Dice set not found.")
    except DiceSetServiceError:
        logger.error(f"Service error while updating dice set {diceset_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.delete("/dicesets/{diceset_id}", response_model=DiceSetPublic)
@limiter.limit("5/minute")
def delete_diceset(
        request: Request,
        diceset_id: int = Path(..., description="The ID of dice set to delete."),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to delete a dice set by ID."""
    try:
        # Check if the user is the owner
        existing_diceset = service.get_diceset(diceset_id)
        if existing_diceset.user_id != current_user.id:
            logger.warning(f"User {current_user.id} tried to delete dice set {diceset_id} not owned by them")
            raise HTTPException(status_code=403, detail="Not allowed")

        logger.info(f"DELETE dice set {diceset_id} by user {current_user.id}")
        deleted = service.delete_diceset(diceset_id)
        return deleted

    except HTTPException:
        raise
    except DiceSetNotFoundError:
        logger.warning(f"Dice set {diceset_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Dice set not found.")
    except DiceSetServiceError:
        logger.error(f"Service error while deleting dice set {diceset_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.post("/dicesets/{diceset_id}/roll", response_model=DiceSetRollResult)
@limiter.limit("30/minute")
def roll_diceset(
        request: Request,
        diceset_id: int = Path(..., description="The ID of the dice set to roll"),
        campaign_id: int = Query(..., description="Campaign ID"),
        dnd_class_id: int = Query(..., description="Class ID"),
        current_user: User = Depends(get_current_user),
        service: DiceSetService = Depends(get_diceset_service)):
    """Endpoint to roll a dice set (only owner allowed)."""
    try:
        # Check ownership first
        diceset = service.get_diceset(diceset_id)

        if diceset.user_id != current_user.id:
            logger.warning(f"User {current_user.id} tried to ROLL dice set {diceset_id} owned by {diceset.user_id}")
            raise HTTPException(status_code=403, detail="Not allowed")

        logger.info(f"ROLL dice set {diceset_id} by user {current_user.id}")
        result = service.roll_diceset(
            current_user.id,
            campaign_id,
            dnd_class_id,
            diceset_id
        )
        return result
    except HTTPException:
        raise
    except DiceSetNotFoundError:
        logger.warning(f"Dice set {diceset_id} not found for roll")
        raise HTTPException(status_code=404, detail="Dice set not found.")
    except DiceSetServiceError:
        logger.error(f"Service error while rolling dice set {diceset_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
