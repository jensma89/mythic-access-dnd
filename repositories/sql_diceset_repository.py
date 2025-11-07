"""
sql_diceset_repository.py

Concrete implementation for sqlalchemy, dice set management.
"""
from typing import List, Optional
from sqlmodel import Session, select, delete
from models.db_models.table_models import Dice, DiceSet, DiceSetDice
from models.schemas.diceset_schema import *
from repositories.diceset_repository import DiceSetRepository
import logging


logger = logging.getLogger(__name__)


class SqlAlchemyDiceSetRepository(DiceSetRepository):
    """Implements the diceset handling methods."""

    def __init__(self, session: Session):
        self.session = session
        logger.debug("SqlAlchemyDiceSetRepository initialized")


    def list_by_user(self, user_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific user."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.user_id == user_id)
        ).all()
        logger.debug(f"Retrieved {len(dicesets)} DiceSets for user {user_id}")
        return [DiceSetPublic.model_validate(d)
                for d in dicesets]


    def list_by_campaign(self, campaign_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific campaign."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.campaign_id == campaign_id)
        ).all()
        logger.debug(f"Retrieved {len(dicesets)} DiceSets for campaign {campaign_id}")
        return [DiceSetPublic.model_validate(d)
                for d in dicesets]


    def list_by_class(self, class_id: int) \
            -> List[DiceSetPublic]:
        """List all dice sets belonging to a specific class."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.class_id == class_id)
        ).all()
        logger.debug(f"Retrieved {len(dicesets)} DiceSets for class {class_id}")
        return [DiceSetPublic.model_validate(d)
                for d in dicesets]


    def get_by_class_id(self, class_id: int) \
            -> List[DiceSetPublic]:
        """Legacy alias for list_by_class."""
        return self.list_by_class(class_id)


    def get_by_id(self, diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Method to get a dice set by ID."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if db_diceset:
            logger.debug(f"Retrieved {db_diceset} for dice set {diceset_id}")
            return DiceSetPublic.model_validate(db_diceset)
        logger.warning(f"Attempted to fetch non-existing DiceSet {diceset_id}")
        return None


    def list_all(self,
                 offset: int = 0,
                 limit: int = 100
                 ) -> List[DiceSetPublic]:
        """Method to get a list of all dice sets."""
        dicesets = self.session.exec(
            select(DiceSet)
            .offset(offset)
            .limit(limit)
        ).all()
        logger.debug(f"Retrieved {len(dicesets)} DiceSets.")
        return [DiceSetPublic.model_validate(d)
                for d in dicesets]


    def add(self, diceset: DiceSetCreate) \
            -> Optional[DiceSetPublic]:
        """Method to add a new dice set."""
        db_diceset = DiceSet(**diceset.model_dump())
        self.session.add(db_diceset)
        self.session.commit()
        self.session.refresh(db_diceset)

        # Add dices (allow duplicates)
        if hasattr(diceset, "dice_ids") and diceset.dice_ids:
            for dice_id in diceset.dice_ids:
                dice = self.session.get(Dice, dice_id)
                if dice:
                    link = DiceSetDice(dice_set_id=db_diceset.id,
                                       dice_id=dice.id)
                    self.session.add(link)
            self.session.commit()
        logger.info(f"DiceSet added: {db_diceset.id} for user {db_diceset.user_id}")
        return DiceSetPublic.model_validate(db_diceset)


    def update(self,
               diceset_id: int,
               diceset: DiceSetUpdate) \
            -> Optional[DiceSetPublic]:
        """Update a dice set."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if not db_diceset:
            logger.warning(f"Attempted to update non-existing DiceSet {diceset_id}")
            return None

        update_data = diceset.model_dump(
            exclude_unset=True)

        # Update normal fields
        for key, value in update_data.items():
            if key != "dice_ids" and hasattr(db_diceset, key):
                setattr(db_diceset, key, value)
        self.session.add(db_diceset)
        self.session.commit()

        # Update dices (allow duplicates)
        if "dice_ids" in update_data:
            # Delete all existing links for this diceset
            self.session.exec(
                delete(DiceSetDice)
                .where(DiceSetDice.dice_set_id == diceset_id))
            self.session.commit()

            # Add new links
            for dice_id in update_data["dice_ids"]:
                dice = self.session.get(Dice, dice_id)
                if dice:
                    link = DiceSetDice(dice_set_id=db_diceset.id,
                                       dice_id=dice.id)
                    self.session.add(link)
            self.session.commit()

        self.session.refresh(db_diceset)
        logger.info(f"Updated DiceSet {diceset_id} for user {db_diceset.user_id}")
        return DiceSetPublic.model_validate(db_diceset)


    def delete(self, diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Remove a dice set."""
        db_diceset = self.session.get(DiceSet, diceset_id)
        if not db_diceset:
            logger.warning(f"Attempted to delete non-existing DiceSet {diceset_id}")
            return None

        # Delete all links first
        self.session.exec(
            delete(DiceSetDice)
            .where(DiceSetDice.dice_set_id == diceset_id))
        self.session.commit()

        # Delete the diceset
        self.session.delete(db_diceset)
        self.session.commit()
        logger.info(f"Deleted DiceSet {diceset_id} for user {db_diceset.user_id}")
        return DiceSetPublic.model_validate(db_diceset)
