"""
class_service.py

Business logic for classes.
"""
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from dependencies import ClassQueryParams
from typing import List, Optional
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository
from repositories.diceset_repository import DiceSetRepository
from repositories.dicelog_repository import DiceLogRepository
import logging



logger = logging.getLogger(__name__)


class ClassService:
    """Business logic
    for class service operations."""

    def __init__(
            self,
            class_repo: ClassRepository,
            diceset_repo: DiceSetRepository,
            dicelog_repo: DiceLogRepository
    ):
        self.class_repo = class_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo
        logger.debug("ClassService initialized")


    def create_class(
            self,
            dnd_class: ClassCreate) \
            -> ClassPublic:
        """Create a new class (max. 4 per campaign)."""
        try:
            #Check the count of classes for a campaign
            existing_classes = (
                self.class_repo
                .get_by_campaign_id(dnd_class.campaign_id))

            if len(existing_classes) >= 4:
                logger.warning(
                    f"Campaign {dnd_class.campaign_id} "
                    f"already has 4 classes"
                )
                raise HTTPException(
                    status_code=400,
                    detail="Campaign already has 4 classes. "
                           "Maximum reached."
                )
            # If limit not reached, create a new class
            new_class = self.class_repo.add(dnd_class)
            if not new_class:
                logger.warning("Class creation failed in repository")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create a new class."
                )
            logger.info(
                f"Created Class {new_class.id} "
                f"- {new_class.name}"
            )
            return new_class

        except SQLAlchemyError:
            logger.exception(
                "Database error "
                "while creating Class",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while create a class."
            )
        except Exception:
            logger.exception(
                "Unexpected error "
                "while creating Class",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error "
                       f"while create a class."
            )


    def get_class(
            self,
            class_id: int) \
            -> Optional[ClassPublic]:
        """Get the class by id."""
        try:
            dnd_class = (self.class_repo
                         .get_by_id(class_id))
            if not dnd_class:
                logger.warning(f"Class {class_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Class with ID {class_id} "
                           f"not found."
                )
            logger.info(
                f"Retrieved Class {class_id} "
                f"- {dnd_class.name}"
            )
            return dnd_class
        except SQLAlchemyError:
            logger.exception(
                f"Database error "
                f"while retrieving Class {class_id}",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while retrieving class."
            )


    def list_classes(
            self,
            filters: ClassQueryParams,
            offset: int = 0,
            limit: int = 100) \
            -> List[ClassPublic]:
        """Get a list of all classes."""
        try:
            classes = self.class_repo.list_all(
                campaign_id=filters.campaign_id,
                name=filters.name,
                offset=offset,
                limit=limit
            )
            logger.info(
                f"Listed {len(classes)} "
                f"Classes (offset={offset},"
                f" limit={limit})"
            )
            return classes
        except SQLAlchemyError:
            logger.exception(
                "Database error "
                "while listing Classes",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while listing classes."
            )


    def update_class(
            self,
            class_id: int,
            dnd_class: ClassUpdate) \
            -> Optional[ClassPublic]:
        """Make changes by a class."""
        try:
            updated_class = self.class_repo.update(
                class_id,
                dnd_class)
            if not updated_class:
                logger.warning(
                    f"Class {class_id} "
                    f"not found for update"
                )
                raise HTTPException(
                    status_code=404,
                    detail=f"Class with ID {class_id} "
                           f"not found."
                )
            logger.info(
                f"Updated Class {class_id} "
                f"- {updated_class.name}"
            )
            return updated_class

        except SQLAlchemyError:
            logger.exception(
                f"Database error "
                f"while updating Class {class_id}",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while updating class."
            )


    def delete_class(
            self,
            class_id: int):
        """Remove a class and the belonging entries:
        dice sets and dice logs."""
        try:
            existing_class = self.class_repo.get_by_id(class_id)
            if not existing_class:
                logger.warning(
                    f"Class {class_id} not found for deletion")
                raise HTTPException(
                    status_code=404,
                    detail=f"Class with ID {class_id} not found."
                )

            # Delete dice logs
            for log in (self.dicelog_repo
                    .list_by_class(class_id)):
                self.dicelog_repo.delete(log.id)

            # Delete dice sets (and their logs)
            for diceset in (self.diceset_repo
                    .list_by_class(class_id)):
                for log in (self.dicelog_repo
                        .list_by_diceset(diceset.id)):
                    self.dicelog_repo.delete(log.id)
                self.diceset_repo.delete(diceset.id)

            # Finally delete class
            deleted_class = self.class_repo.delete(class_id)
            if not deleted_class:
                logger.warning(f"Failed to delete Class {class_id}")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete class."
                )
            logger.info(
                f"Deleted Class {class_id} "
                f"- {deleted_class}"
            )
            return deleted_class

        except SQLAlchemyError:
            logger.exception(
                f"Database error "
                f"while deleting Class {class_id}",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Database error "
                       f"while deleting class."
            )
        except Exception:
            logger.exception(
                f"Unexpected error "
                f"while deleting Class {class_id}",
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error "
                       f"while deleting class."
            )
