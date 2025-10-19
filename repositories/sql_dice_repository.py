"""
sql_dice_repository.py

Concrete implementation of sqlalchemy, dice management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import Dice
from models.schemas.dice_schema import *
from repositories.dice_repository import DiceRepository


class SqlAlchemyDiceRepository(DiceRepository):
    """This class implement
    the class handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, dice_id: int) -> Optional[DicePublic]:
        """Method to get dice by ID."""
        db_dice = self.session.get(Dice, dice_id)
        if db_dice:
            return DicePublic.model_validate(db_dice)
        return None


    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[DicePublic]:
        """Method to show all dices."""
        dices = self.session.exec(
            select(Dice)
            .offset(offset)
            .limit(limit)).all()
        return [DicePublic.model_validate(d) for d in dices]


    def add(self, dice: DiceCreate) -> DicePublic:
        """Method to create a new dice."""
        db_dice = Dice(**dice.model_dump())
        self.session.add(db_dice)
        self.session.commit()
        self.session.refresh(db_dice)
        return DicePublic.model_validate(db_dice)


    def update(self, dice_id: int,
               dice: DiceUpdate) -> Optional[DicePublic]:
        """Method to change data from a dice."""
        db_dice = self.session.get(Dice, dice_id)
        if not db_dice:
            return None
        for key, value in dice.model_dump(exclude_unset=True).items():
            setattr(db_dice, key, value)
        self.session.add(db_dice)
        self.session.commit()
        self.session.refresh(db_dice)
        return DicePublic.model_validate(db_dice)


    def delete(self, dice_id: int) -> Optional[DicePublic]:
        """Method to remove a dice."""
        db_dice = self.session.get(Dice, dice_id)
        if not db_dice:
            return None
        self.session.delete(db_dice)
        self.session.commit()
        return DicePublic.model_validate(db_dice)


    def get_by_class_id(self, class_id: int) -> List[DicePublic]:
        """Get all dices belonging to a class."""
        dices = self.session.exec(
            select(Dice).where(Dice.class_id == class_id)
        ).all()
        return [DicePublic.model_validate(d) for d in dices]
