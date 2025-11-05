"""
dicelogs.py

API endpoints for dice log management.
"""
from fastapi import APIRouter, Depends, HTTPException, Path
from dependencies import Pagination, SessionDep
from models.schemas.dicelog_schema import *
from repositories.sql_dicelog_repository import *
from auth.auth import get_current_user
from models.db_models.table_models import User



router = APIRouter(tags=["dicelogs"])


def get_dicelog_repo(session: SessionDep):
    """Factory to get the dice log repo."""
    return SqlAlchemyDiceLogRepository(session)



@router.get("/dicelogs/",
            response_model=List[DiceLogPublic])
def list_logs(
        user_id: int,
        pagination: Pagination = Depends(),
        dicelog_repo: SqlAlchemyDiceLogRepository = Depends(get_dicelog_repo)):
    """Endpoint to list all dice logs
    by a specific user."""
    return dicelog_repo.list_logs(
        user_id=user_id,
        offset=pagination.offset,
        limit=pagination.limit)


@router.get("/dicelogs/{dicelog_id}",
            response_model=DiceLogPublic)
def get_log(
        dicelog_id: int,
        repo: SqlAlchemyDiceLogRepository = Depends(get_dicelog_repo)):
    """Endpoint to get a single dice log by ID."""
    dicelog = repo.get_by_id(dicelog_id)
    if not dicelog:
        raise HTTPException(
            status_code=404,
            detail="Dice log not found.")
    return dicelog
