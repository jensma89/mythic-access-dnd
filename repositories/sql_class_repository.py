"""
sql_class_repository.py

Concrete implementation for sqlalchemy, class management.
"""
from fastapi import Query
from typing import List, Optional, Annotated
from sqlmodel import Session, select
from models.db_models.table_models import Class
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository



class SqlAlchemyClassRepository(ClassRepository):
    """This class implement
        the class handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, class_id: int) -> Optional[ClassPublic]:
        """Method to get a class by ID."""
        db_class = self.session.get(Class, class_id)
        if db_class:
            return ClassPublic.model_validate(db_class)
        return None


    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[ClassPublic]:
        """Method to show all classes."""
        classes = self.session.exec(
            select(Class)
            .offset(offset)
            .limit(limit)).all()
        return [ClassPublic.model_validate(c) for c in classes]


    def add(self, new_class: ClassCreate) -> ClassPublic:
        """Method to create a new class."""
        db_class = Class(**new_class.model_dump())
        self.session.add(db_class)
        self.session.commit()
        self.session.refresh(db_class)
        return ClassPublic.model_validate(db_class)


    def update(self, class_id: int,
               update_class: ClassUpdate) -> Optional[ClassPublic]:
        """Method to change data from a class."""
        db_class = self.session.get(Class, class_id)
        if not db_class:
            return None
        for key, value in update_class.model_dump(exclude_unset=True).items():
            setattr(db_class, key, value)
        self.session.add(db_class)
        self.session.commit()
        self.session.refresh(db_class)
        return ClassPublic.model_validate(db_class)


    def delete(self, class_id: int) -> Optional[ClassPublic]:
        """Method to remove a class."""
        db_class = self.session.get(Class, class_id)
        if not db_class:
            return None
        self.session.delete(db_class)
        self.session.commit()
        return ClassPublic.model_validate(db_class)
