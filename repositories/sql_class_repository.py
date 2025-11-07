"""
sql_class_repository.py

Concrete implementation for sqlalchemy, class management.
"""
from typing import List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import Class, Campaign
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository
import logging



logger = logging.getLogger(__name__)


class SqlAlchemyClassRepository(ClassRepository):
    """This class implement
        the class handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session
        logger.debug("SqlAlchemyClassRepository initialized")


    def list_by_user(self, user_id: int) \
            -> List[ClassPublic]:
        """List all classes belonging to a specific user."""
        dnd_classes = self.session.exec(
            select(Class)
            .join(Campaign)
            .where(Campaign.created_by == user_id)
        ).all()
        logger.debug(f"Retrieved {len(dnd_classes)} classes for user {user_id}")
        return [ClassPublic.model_validate(c)
                for c in dnd_classes]


    def list_by_campaign(self, campaign_id: int) \
            -> List[ClassPublic]:
        """List all classes belonging to a specific campaign."""
        dnd_classes = self.session.exec(
            select(Class)
            .where(Class.campaign_id == campaign_id)
        ).all()
        logger.debug(f"Retrieved {len(dnd_classes)} classes for campaign {campaign_id}")
        return [ClassPublic.model_validate(c)
                for c in dnd_classes]


    def list_by_class(self, class_id: int) \
            -> List[ClassPublic]:
        """Return a single class as list."""
        dnd_class = self.session.exec(
            select(Class)
            .where(Class.id == class_id)
        ).all()
        logger.debug(f"Retrieved {len(dnd_class)} records for class_id {class_id}")
        return [ClassPublic.model_validate(c)
                for c in dnd_class]


    def get_by_campaign_id(self, campaign_id: int) \
            -> List[ClassPublic]:
        """Legacy alias for list_by_campaign."""
        return self.list_by_campaign(campaign_id)


    def get_by_id(self, class_id: int) \
            -> Optional[ClassPublic]:
        """Method to get a class by ID."""
        db_class = self.session.get(Class, class_id)
        if db_class:
            logger.debug(f"Class found: {class_id} - {db_class.name}")
            return ClassPublic.model_validate(db_class)
        logger.warning(f"Class not found: {class_id}")
        return None


    def list_all(self,
                 offset: int = 0,
                 limit: int = 100,
                 campaign_id: Optional[int] = None,
                 name: Optional[str] = None
                 ) -> List[ClassPublic]:
        """Method to show all classes
        with optional campaign or name filter."""
        query = select(Class)

        if name:
            query = (
                query
                .where(Class.name.ilike(f"%{name}%")))
        if campaign_id:
            query = (
                query
                .where(Class.campaign_id == campaign_id))

        classes = self.session.exec(
            query.offset(offset)
            .limit(limit)).all()
        logger.debug(f"Listed {len(classes)} classes with filters name={name}, campaign_id={campaign_id}")
        return [ClassPublic.model_validate(c)
                for c in classes]


    def add(self, dnd_class: ClassCreate) \
            -> ClassPublic:
        """Method to create a new class."""
        db_class = Class(**dnd_class.model_dump())
        self.session.add(db_class)
        self.session.commit()
        self.session.refresh(db_class)
        logger.info(f"Class added: {db_class.id} - {db_class.name}")
        return ClassPublic.model_validate(db_class)


    def update(self,
               class_id: int,
               dnd_class: ClassUpdate) \
            -> Optional[ClassPublic]:
        """Method to change data from a class."""
        db_class = self.session.get(Class, class_id)
        if not db_class:
            logger.warning(f"Attempted to update non-existing class {class_id}")
            return None
        for key, value in dnd_class.model_dump(
                exclude_unset=True).items():
            setattr(db_class, key, value)
        self.session.add(db_class)
        self.session.commit()
        self.session.refresh(db_class)
        logger.info(f"Updated class: {class_id} - {db_class.name}")
        return ClassPublic.model_validate(db_class)


    def delete(self, class_id: int) \
            -> Optional[ClassPublic]:
        """Method to remove a class."""
        db_class = self.session.get(Class, class_id)
        if not db_class:
            logger.warning(f"Attempted to delete non-existing class {class_id}")
            return None
        self.session.delete(db_class)
        self.session.commit()
        logger.info(f"Deleted class: {class_id} - {db_class.name}")
        return ClassPublic.model_validate(db_class)
