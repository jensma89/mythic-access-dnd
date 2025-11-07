"""
classes.py

The API endpoints for classes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from dependencies import ClassQueryParams, Pagination, SessionDep
from models.schemas.class_schema import *
from services.class_service import ClassService
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from auth.auth import get_current_user
from models.db_models.table_models import User
from rate_limit import limiter


router = APIRouter(tags=["classes"])



def get_class_service(session: SessionDep) \
        -> ClassService:
    """Factory to get the class, dice set and dice log service."""
    class_repo = SqlAlchemyClassRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)
    dicelog_repo = SqlAlchemyDiceLogRepository(session)
    return ClassService(
        class_repo,
        diceset_repo,
        dicelog_repo
    )


@router.get("/classes/{class_id}",
            response_model=ClassPublic)
@limiter.limit("10/minute")
def read_class(
        request: Request,
        class_id: int = Path(..., description="The ID of the class to retrieve."),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to get a single dnd class."""
    dnd_class = service.get_class(class_id)
    if not dnd_class:
        raise HTTPException(
            status_code=404,
            detail="Class not found.")
    return dnd_class


@router.get("/classes/",
            response_model=List[ClassPublic])
@limiter.limit("10/minute")
def read_classes(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        filters: ClassQueryParams = Depends(),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to get a list of all classes."""
    return service.list_classes(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters)


@router.post("/classes/",
             response_model=ClassPublic)
@limiter.limit("3/minute")
def create_class(
        request: Request,
        dnd_class: ClassCreate,
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to create a new class."""
    return service.create_class(dnd_class)


@router.patch("/classes/{class_id}",
            response_model=ClassPublic)
@limiter.limit("3/minute")
def update_class(
        request: Request,
        dnd_class: ClassUpdate,
        class_id: int = Path(..., description="The ID of the class to update."),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to make changes by a class."""
    updated = service.update_class(class_id, dnd_class)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Class not found.")
    return updated


@router.delete("/classes/{class_id}",
               response_model=ClassPublic)
@limiter.limit("5/minute")
def delete_class(
        request: Request,
        class_id: int = Path(..., description="The ID of the class to delete."),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to delete a class by ID."""
    deleted = service.delete_class(class_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Class not found.")
    return deleted
