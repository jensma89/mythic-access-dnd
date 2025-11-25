"""
classes.py

The API endpoints for classes.
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from typing import List
import logging

from dependencies import ClassQueryParams, Pagination, SessionDep
from services.class_service import ClassService
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from models.db_models.table_models import User
from models.schemas.class_schema import *
from auth.auth import get_current_user
from rate_limit import limiter


router = APIRouter(tags=["classes"])
logger = logging.getLogger(__name__)



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
        class_id: int = Path(
            ...,
            description="The ID of the class to retrieve."
        ),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)
):
    """Endpoint to get a single dnd class."""
    logger.info(
        f"GET class {class_id} "
        f"by user {current_user.id}"
    )
    dnd_class = service.get_class(class_id)
    if not dnd_class:
        logger.warning(f"Class {class_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Class not found.")

    if dnd_class.user_id != current_user.id:
        logger.warning(
            f"User {current_user.id} tried to access "
            f"class {class_id} not owned by them"
        )
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )
    return dnd_class


@router.get("/classes/",
            response_model=List[ClassPublic])
@limiter.limit("10/minute")
def read_classes(
        request: Request,
        current_user: User = Depends(get_current_user),
        pagination: Pagination = Depends(),
        filters: ClassQueryParams = Depends(),
        service: ClassService = Depends(get_class_service)
):
    """Endpoint to get a list of all classes."""
    logger.info(f"GET classes list "
                f"by user {current_user.id}"
                )
    filters.user_id = current_user.id
    return service.list_classes(
        offset=pagination.offset,
        limit=pagination.limit,
        filters=filters)


@router.post("/classes/",
             response_model=ClassPublic)
@limiter.limit("3/minute")
def create_class(
        request: Request,
        dnd_class_input: ClassCreateInput,
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)
):
    """Endpoint to create a new class."""
    logger.info(f"POST create class "
                f"by user {current_user.id}"
                )

    # Set current user as owner
    dnd_class_create = ClassCreate(**dnd_class_input.model_dump())
    dnd_class_create.set_user(current_user.id)
    created = service.create_class(dnd_class_create)
    logger.info(
        f"Class {created.id} "
        f"created by user {current_user.id}"
    )
    return created


@router.patch("/classes/{class_id}",
            response_model=ClassPublic)
@limiter.limit("3/minute")
def update_class(
        request: Request,
        dnd_class: ClassUpdate,
        class_id: int = Path(
            ...,
            description="The ID of the class to update."
        ),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to change class data."""

    # Check if the user is the owner
    existing_class = service.get_class(class_id)
    if existing_class.user_id != current_user.id:
        logger.warning(
            f"User {current_user.id} tried to "
            f"update class {class_id} "
            f"not owned by them"
        )
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    logger.info(
        f"PATCH update class {class_id} "
        f"by user {current_user.id}"
    )
    updated = service.update_class(class_id, dnd_class)
    if not updated:
        logger.warning(f"Class {class_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Class not found.")
    return updated


@router.delete("/classes/{class_id}",
               response_model=ClassPublic)
@limiter.limit("5/minute")
def delete_class(
        request: Request,
        class_id: int = Path(
            ...,
            description="The ID of the class to delete."
        ),
        current_user: User = Depends(get_current_user),
        service: ClassService = Depends(get_class_service)):
    """Endpoint to delete a class by ID."""

    # Check if the user is the owner
    existing_class = service.get_class(class_id)
    if existing_class.user_id != current_user.id:
        logger.warning(
            f"User {current_user.id} tried to "
            f"delete class {class_id} "
            f"not owned by them"
        )
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    logger.info(
        f"DELETE class {class_id} "
        f"by user {current_user.id}"
    )
    deleted = service.delete_class(class_id)
    if not deleted:
        logger.warning(f"Class {class_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Class not found.")
    return deleted
