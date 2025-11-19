"""
diceset_service.py

Business logic for dice sets.
"""
from datetime import datetime, timezone
from random import randint
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models.schemas.diceset_schema import *
from repositories.diceset_repository import *
from repositories.dice_repository import *
from repositories.dicelog_repository import *
from models.schemas.dicelog_schema import *
import logging



logger = logging.getLogger(__name__)


class DiceSetService:
    """Business logic for dice set service."""

    def __init__(
            self,
            dice_repo: DiceRepository,
            diceset_repo: DiceSetRepository,
            dicelog_repo: DiceLogRepository):
        self.dice_repo = dice_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo
        logger.debug("DiceSetService initialized")


    def create_diceset(
            self,
            diceset: DiceSetCreate) \
            -> DiceSetPublic:
        """Create a new dice set
        (optionally with existing dice)."""
        try:
            # Validation max 5 sets per dnd class
            existing_sets = (
                self.diceset_repo
                .get_by_class_id(diceset.class_id))
            logger.info(f"Creating DiceSet for Class {diceset.class_id}. "
                        f"Existing sets: {len(existing_sets)}")
            if len(existing_sets) >= 5:
                logger.warning(f"Cannot create DiceSet for Class {diceset.class_id}: max 5 sets reached")
                raise HTTPException(
                    status_code=400,
                    detail="Maximum of 5 dice sets "
                           "per class reached.")

            # Check for existing dice IDs
            if self.dice_repo and diceset.dice_ids:
                for dice_id in diceset.dice_ids:
                    if not self.dice_repo.get_by_id(dice_id):
                        logger.warning(f"Dice ID {dice_id} not found for new DiceSet")
                        raise HTTPException(
                            status_code=404,
                            detail=f"Dice {dice_id} "
                                   f"not found.")

            # Create the dice set itself
            created = self.diceset_repo.add(diceset)
            logger.info(f"Created DiceSet {created.id} - {created.name} for Class {diceset.class_id}")

            # Handle multiple dice (if same dice appear multiple times)
            if diceset.dice_ids:
                dice_count = {}
                for dice_id in diceset.dice_ids:
                    dice_count[dice_id] = dice_count.get(dice_id, 0) + 1

                for dice_id, quantity, in dice_count.items():
                    for _ in range (quantity):
                        self.diceset_repo.add_dice_to_set(
                            diceset_id=created.id,
                            dice_id=dice_id
                        )
                        logger.debug(f"Added dice {dice_id} x1 to dice set {created.id}")


        except SQLAlchemyError:
            logger.exception("Database error while creating DiceSet", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while creating dice set."
            )
        except Exception:
            logger.exception("Unexpected error while creating DiceSet", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while creating dice set."
            )


    def get_diceset(
            self,
            diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Get a dice set by ID."""
        try:
            db_diceset = (self.diceset_repo
                          .get_by_id(diceset_id))
            if not db_diceset:
                logger.warning(f"DiceSet {diceset_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice set with ID {diceset_id} "
                           f"not found."
                )
            logger.info(f"Retrieved DiceSet {diceset_id} - {db_diceset.name}")
            return db_diceset

        except SQLAlchemyError:
            logger.exception(f"Database error while fetching DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while fetching dice set."
            )
        except Exception:
            logger.exception(f"Unexpected error while fetching DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while fetching dice set."
            )


    def list_dicesets(
            self,
            offset: int = 0,
            limit: int = 100) \
            -> List[DiceSetPublic]:
        """Get a list of all dice sets."""
        try:
            return self.diceset_repo.list_all(
                offset=offset,
                limit=limit)
        except SQLAlchemyError:
            logger.exception("Database error while listing DiceSets", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while listing dice sets."
            )
        except Exception:
            logger.exception("Unexpected error while listing DiceSets", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while listing dice sets."
            )


    def update_diceset(
            self,
            diceset_id: int,
            diceset: DiceSetUpdate) \
            -> Optional[DiceSetPublic]:
        """Change data from a dice set."""
        try:
            updated = self.diceset_repo.update(
                diceset_id,
                diceset)
            if not updated:
                logger.warning(f"DiceSet {diceset_id} not found for update")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice set with ID {diceset_id} "
                           f"not found."
                )
            logger.info(f"Updated DiceSet {diceset_id} - {updated.name}")
            return updated

        except SQLAlchemyError:
            logger.exception(f"Database error while updating DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while updating dice set."
            )
        except Exception:
            logger.exception(f"Unexpected error while updating DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while updating dice set."
            )


    def delete_diceset(
            self,
            diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Remove a class and the belonging entries:
        dice sets and dice logs."""
        try:
            # Delete dice logs
            logs = (self.dicelog_repo
                    .list_by_diceset(diceset_id))
            for log in logs:
                self.dicelog_repo.delete(log.id)
                logger.info(f"Deleted DiceLog {log.id} from DiceSet {diceset_id}")

            # Finally delete diceset
            deleted = self.diceset_repo.delete(diceset_id)
            if not deleted:
                logger.warning(f"DiceSet {diceset_id} not found for deletion")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice set with ID {diceset_id} "
                           f"not found."
                )
            logger.info(f"Deleted DiceSet {diceset_id} - {deleted.name}")
            return deleted

        except SQLAlchemyError:
            logger.exception(f"Database error while deleting DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while deleting dice set."
            )
        except Exception:
            logger.exception(f"Unexpected error while deleting DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while deleting dice set."
            )


    def _log_roll(
            self,
            user_id: int,
            campaign_id: int,
            class_id: int,
            diceset_id: int,
            name: str,
            results: list,
            total: int):
        """Function for dice set log entrys."""
        if not self.dicelog_repo:
            logger.warning("DiceLogRepository not provided, skipping roll log")
            return
        try:
            log_entry = DiceLogCreate(
                user_id=user_id,
                campaign_id=campaign_id,
                class_id=class_id,
                diceset_id=diceset_id,
                roll=f"{name}: {[r.result for r in results]}",
                result=total,
                timestamp=datetime.now(timezone.utc)
            )
            self.dicelog_repo.log_roll(log_entry)
            logger.info(f"Logged DiceSet roll for DiceSet {diceset_id} by User {user_id}")
        except SQLAlchemyError:
            logger.exception(f"Database error while logging roll for DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while logging dice set roll."
            )
        except Exception:
            logger.exception(f"Unexpected error while logging roll for DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while logging dice set roll."
            )


    def roll_diceset(
            self,
            user_id: int,
            campaign_id: int,
            class_id: int,
            diceset_id: int):
        """Roll all dices in a set
        and return each result + total sum."""
        try:
            diceset = (self.diceset_repo
                       .get_by_id(diceset_id))
            if not diceset or not diceset.dices:
                logger.warning(f"DiceSet {diceset_id} not found or has no dices")
                raise HTTPException(
                    status_code=404,
                    detail="Dice set not found "
                           "or has no dices.")
            results = []
            total_sum = 0

            for dice in diceset.dices:
                roll_value = randint(1, dice.sides) # E.g. sides 6 or 12
                results.append(DiceRollResult(
                    id=dice.id,
                    name=dice.name,
                    sides=dice.sides,
                    result=roll_value
                ))
                total_sum += roll_value

            logger.info(f"Rolled DiceSet {diceset_id} by User {user_id}: "
                        f"Results {[r.result for r in results]}, Total: {total_sum}")

            self._log_roll(
                user_id,
                campaign_id,
                class_id,
                diceset_id,
                diceset.name,
                results,
                total_sum
            )

            return DiceSetRollResult(
                diceset_id=diceset.id,
                name=diceset.name,
                results=results,
                total=total_sum
            )
        except SQLAlchemyError:
            logger.exception(f"Database error while rolling DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while rolling dice set."
            )
        except Exception:
            logger.exception(f"Unexpected error while rolling DiceSet {diceset_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while rolling dice set."
            )
