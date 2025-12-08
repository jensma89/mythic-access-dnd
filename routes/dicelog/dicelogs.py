"""
dicelogs.py

API endpoints for dice log management.
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from dependencies import Pagination, SessionDep
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from models.schemas.dicelog_schema import DiceLogPublic
from typing import List
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter
import logging


router = APIRouter(tags=["dicelogs"])
logger = logging.getLogger(__name__)


def get_dicelog_repo(session: SessionDep):
    """Factory to get the dice log repo."""
    return SqlAlchemyDiceLogRepository(session)


@router.get("/dicelogs/", response_model=List[DiceLogPublic])
@limiter.limit("10/minute")
def list_logs(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        dicelog_repo: SqlAlchemyDiceLogRepository = Depends(get_dicelog_repo)):
    """Endpoint to list all dice logs for the current user."""
    logger.info(f"GET logs for user {current_user.id}")
    try:
        logs = dicelog_repo.list_logs(
            user_id=current_user.id,
            offset=pagination.offset,
            limit=pagination.limit
        )
        logger.info(f"Returned {len(logs)} logs for user {current_user.id}")
        return logs

    except Exception:
        logger.exception("Error while listing dice logs")
        raise HTTPException(
            status_code=500,
            detail="Error while listing dice logs."
        )


@router.get("/dicelogs/{dicelog_id}", response_model=DiceLogPublic)
@limiter.limit("10/minute")
def get_log(
        request: Request,
        dicelog_id: int = Path(..., description="The log ID to retrieve."),
        current_user: User = Depends(get_current_user),
        repo: SqlAlchemyDiceLogRepository = Depends(get_dicelog_repo)):
    """Endpoint to get a single dice log by ID (only if owned by current user)."""
    logger.info(f"GET log {dicelog_id} by user {current_user.id}")
    try:
        dicelog = repo.get_by_id(dicelog_id)
        if not dicelog:
            logger.warning(f"Dice log {dicelog_id} not found")
            raise HTTPException(
                status_code=404,
                detail="Dice log not found."
            )

        if dicelog.user_id != current_user.id:
            logger.warning(
                f"User {current_user.id} tried to access "
                f"log {dicelog_id} not owned by them"
            )
            raise HTTPException(
                status_code=403,
                detail="Not allowed."
            )
        return dicelog

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Error while fetching dice log {dicelog_id}")
        raise HTTPException(
            status_code=500,
            detail="Error while fetching dice log."
        )
