"""
sql_diceset_repository.py

Concrete implementation for sqlalchemy, dice set management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import DiceSet
from models.schemas.diceset_schema import *
from repositories.diceset_repository import DiceSetRepository


class SqlAlchemyDiceSetRepository(DiceSetRepository):
    """This class implement
        the diceset handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, diceset_id: int) -> Optional[DiceSetPublic]:
        """Method to get the dice set by ID."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if db_diceset:
            return DiceSetPublic.model_validate(db_diceset)
        return None


    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[DiceSetPublic]:
        """Method to show all dice sets."""
        dicesets = self.session.exec(
            select(DiceSet)
            .offset(offset)
            .limit(limit)).all()
        return [DiceSetPublic.model_validate(d) for d in dicesets]


    def add(self, diceset: DiceSetCreate) -> Optional[DiceSetPublic]:
        """Method to create a new dice set."""
        db_diceset = DiceSet(**diceset.model_dump())
        self.session.add(db_diceset)
        self.session.commit()
        self.session.refresh(db_diceset)
        return DiceSetPublic.model_validate(db_diceset)


    def update(self,
               diceset_id: int,
               diceset: DiceSetUpdate) -> Optional[DiceSetPublic]:
        """Method to update a dice set."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if not db_diceset:
            return None
        for key, value in diceset.model_dump(exclude_unset=True).items():
            setattr(db_diceset, key, value)
        self.session.add(db_diceset)
        self.session.commit()
        self.session.refresh(db_diceset)
        return DiceSetPublic.model_validate(db_diceset)


    def delete(self, diceset_id: int) -> Optional[DiceSetPublic]:
        """Method to remove a dice set by ID."""
        db_diceset: self.session.get(DiceSet, diceset_id)
        if not db_diceset:
            return None
        self.session.delete(db_diceset)
        self.session.commit()
        return DiceSetPublic.model_validate(db_diceset)


    def get_by_class_id(self, class_id: int) -> List[DiceSetPublic]:
        """Get all dice sets belonging to a class."""
        dices = self.session.exec(
            select(DiceSet).where(DiceSet.class_id == class_id)
        ).all()
        return [DiceSetPublic.model_validate(d) for d in dices]
