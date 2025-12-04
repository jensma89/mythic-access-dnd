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
        """List all dice sets belonging to a specific dnd_class."""
        dicesets = self.session.exec(
            select(DiceSet)
            .where(DiceSet.class_id == class_id)
        ).all()
        logger.debug(f"Retrieved {len(dicesets)} DiceSets for dnd_class {class_id}")
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
        if not db_diceset:
            logger.warning(f"Attempted to fetch non-existing DiceSet {diceset_id}")
            return None

        expanded_dices = []
        for entry in getattr(db_diceset, "dice_entries", []) or []:
            if not getattr(entry, "dice", None):
                dice_obj = self.session.get(Dice, entry.dice_id)
            else:
                dice_obj = entry.dice
            if dice_obj:
                for _ in range(entry.quantity or 1):
                    expanded_dices.append(dice_obj)

        payload = {
            "id": db_diceset.id,
            "name": db_diceset.name,
            "user_id": db_diceset.user_id,
            "dices": [  # DicePublic expects id,name,sides
                {"id": d.id, "name": d.name, "sides": d.sides}
                for d in expanded_dices
            ]
        }
        logger.debug(f"Retrieved {db_diceset} for dice set {diceset_id} with expanded dices {len(expanded_dices)}")
        return DiceSetPublic.model_validate(payload)


    def get_orm_by_id(self, diceset_id: int) -> Optional[DiceSet]:
        """Return ORM DiceSet object (with dice_entries)"""
        return self.session.get(DiceSet, diceset_id)



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


    def add(self, diceset: DiceSetCreate) -> Optional[DiceSetPublic]:
        """Method to add a new dice set."""
        db_diceset = DiceSet(**diceset.model_dump())
        self.session.add(db_diceset)
        self.session.commit()
        self.session.refresh(db_diceset)

        logger.info(f"DiceSet added: {db_diceset.id} for user {db_diceset.user_id}")
        return self.get_by_id(db_diceset.id)


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

            # Count duplicates
            dice_count = {}
            for dice_id in update_data["dice_ids"]:
                dice_count[dice_id] = dice_count.get(dice_id, 0) + 1

            # Add new links with quantity
            for dice_id, quantity in dice_count.items():
                dice = self.session.get(Dice, dice_id)
                if dice:
                    entry = DiceSetDice(
                        dice_set_id=db_diceset.id,
                        dice_id=dice.id,
                        quantity=quantity
                    )
                    self.session.add(entry)
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


    def set_dice_quantities(self, diceset_id: int, dice_count: dict):
        """Store dice quantities for a dice set."""
        session = self.session

        # Delete existing entries to fully rebuild
        session.exec(
            delete(DiceSetDice).where(DiceSetDice.dice_set_id == diceset_id)
        )
        session.commit()

        # Insert each dice with correct quantity
        for dice_id, quantity in dice_count.items():
            entry = DiceSetDice(
                dice_set_id=diceset_id,
                dice_id=dice_id,
                quantity=quantity
            )
            session.add(entry)

        session.commit()
