"""
sql_diceset_repository.py

Concrete implementation for sqlalchemy, dice set management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import Dice, DiceSet
from models.schemas.diceset_schema import *
from repositories.diceset_repository import DiceSetRepository


class SqlAlchemyDiceSetRepository(DiceSetRepository):
    """This class implement
        the diceset handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session


    def list_by_user(self, user_id: int) -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific user."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.user_id == user_id)
        ).all()
        return [DiceSetPublic.model_validate(d) for d in dicesets]


    def list_by_campaign(self, campaign_id: int) -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific campaign."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.campaign_id == campaign_id)
        ).all()
        return [DiceSetPublic.model_validate(d) for d in dicesets]


    def list_by_class(self, class_id: int) -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific DnD class."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.class_id == class_id)
        ).all()
        return [DiceSetPublic.model_validate(d) for d in dicesets]


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

        update_data = diceset.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(db_diceset, key):
                setattr(db_diceset, key, value)

        # If dice_id updated, set the relationship
        if "dice_ids" in update_data:
            db_diceset.dices.clear()
            for dice_id in update_data["dice_ids"]:
                dice = self.session.get(Dice, dice_id)
                if dice:
                    db_diceset.dices.append(dice)

        self.session.add(db_diceset)
        self.session.commit()
        self.session.refresh(db_diceset)
        return DiceSetPublic.model_validate(db_diceset)


    def delete(self, diceset_id: int) -> Optional[DiceSetPublic]:
        """Method to remove a dice set by ID."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if not db_diceset:
            return None
        self.session.delete(db_diceset)
        self.session.commit()
        return DiceSetPublic.model_validate(db_diceset)
