"""
sql_dice_repository.py

Concrete implementation of sqlalchemy, dice management.
"""
from sqlmodel import Session, select
from models.db_models.table_models import Dice
from models.schemas.dice_schema import *
from repositories.dice_repository import DiceRepository
from typing import List, Optional
import logging



logger = logging.getLogger(__name__)


class SqlAlchemyDiceRepository(DiceRepository):
    """This dnd_class implement
    the dice handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session
        logger.debug("SqlAlchemyDiceRepository initialized")


    def get_by_id(self, dice_id: int) \
            -> Optional[DicePublic]:
        """Method to get dice by ID."""
        db_dice = self.session.get(Dice, dice_id)
        if db_dice:
            logger.debug(f"Dice found: {dice_id} - {db_dice.name}")
            return DicePublic.model_validate(db_dice)
        logger.warning(f"Dice not found: {dice_id}")
        return None


    def list_all(self,
                 offset: int = 0,
                 limit: int = 100
                 ) -> List[DicePublic]:
        """Method to show all dices."""
        dices = self.session.exec(
            select(Dice)
            .offset(offset)
            .limit(limit)).all()
        logger.debug(f"Listed {len(dices)} dices (offset={offset}, limit={limit})")
        return [DicePublic.model_validate(d)
                for d in dices]


    def add(self, dice: DiceCreate) \
            -> DicePublic:
        """Method to create a new dice."""
        db_dice = Dice(**dice.model_dump())
        self.session.add(db_dice)
        self.session.commit()
        self.session.refresh(db_dice)
        logger.info(f"Dice added: {db_dice.id} - {db_dice.name}")
        return DicePublic.model_validate(db_dice)


    def update(self,
               dice_id: int,
               dice: DiceUpdate) \
            -> Optional[DicePublic]:
        """Method to change data from a dice."""
        db_dice = self.session.get(Dice, dice_id)
        if not db_dice:
            logger.warning(f"Attempted to update non-existing dice {dice_id}")
            return None

        for key, value in dice.model_dump(
                exclude_unset=True).items():
            setattr(db_dice, key, value)
        self.session.add(db_dice)
        self.session.commit()
        self.session.refresh(db_dice)
        logger.info(f"Updated dice: {dice_id} - {db_dice.name}")
        return DicePublic.model_validate(db_dice)


    def delete(self, dice_id: int) \
            -> Optional[DicePublic]:
        """Method to remove a dice."""
        db_dice = self.session.get(Dice, dice_id)
        if not db_dice:
            logger.warning(f"Attempted to delete non-existing dice {dice_id}")
            return None
        self.session.delete(db_dice)
        self.session.commit()
        logger.info(f"Deleted dice: {dice_id} - {db_dice.name}")
        return DicePublic.model_validate(db_dice)


    def get_by_class_id(self, class_id: int) \
            -> List[DicePublic]:
        """Get all dices belonging to a dnd_class."""
        dices = self.session.exec(
            select(Dice)
            .where(Dice.class_id == class_id)
        ).all()
        logger.debug(f"Retrieved {len(dices)} dices for dnd_class {class_id}")
        return [DicePublic.model_validate(d)
                for d in dices]
