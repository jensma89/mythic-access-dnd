"""
dice_service.py

Business logic for dice handling.
"""
from random import randint
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models.schemas.dice_schema import *
from models.schemas.dicelog_schema import *
from repositories.dice_repository import DiceRepository
from repositories.dicelog_repository import DiceLogRepository
import logging



logger = logging.getLogger(__name__) # hier weitermachen


class DiceService:
    """Business logic
    for dice service operations."""

    def __init__(
            self,
            repository: DiceRepository,
            log_repository: Optional[DiceLogRepository] = None):
        self.repo = repository
        self.log_repo = log_repository
        logger.debug("DiceService initialized")


    def create_dice(self, dice: DiceCreate) \
            -> Optional[DicePublic]:
        """Create a new dice."""
        try:
            created = self.repo.add(dice)
            logger.info(f"Created Dice {created.id} - {created.name}")
            return created
        except SQLAlchemyError:
            logger.exception("Database error while creating Dice", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while creating dice."
            )
        except Exception:
            logger.exception("Unexpected error while creating Dice", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while creating dice."
            )


    def get_dice(self, dice_id: int) \
            -> Optional[DicePublic]:
        """Get the dice by ID."""
        try:
            db_dice = self.repo.get_by_id(dice_id)
            if not db_dice:
                logger.warning(f"Dice {dice_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            logger.info(f"Retrieved Dice {dice_id} - {db_dice.name}")
            return db_dice
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while fetching dice."
            )
        except Exception:
            logger.exception(f"Unexpected error while fetching Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while fetching dice."
            )


    def list_dices(
            self,
            offset: int = 0,
            limit: int = 100) \
            -> List[DicePublic]:
        """Get a list of all dices."""
        try:
            dices = self.repo.list_all(
                offset=offset,
                limit=limit)
            logger.info(f"Listed {len(dices)} Dices (offset={offset}, limit={limit})")
            return dices
        except SQLAlchemyError:
            logger.exception("Database error while listing Dices", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while listing dices."
            )
        except Exception:
            logger.exception("Unexpected error while listing Dices", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while listing dices."
            )


    def update_dice(
            self,
            dice_id: int,
            dice: DiceUpdate) \
            -> Optional[DicePublic]:
        """Change the data from a dice."""
        try:
            updated = self.repo.update(dice_id, dice)
            if not updated:
                logger.warning(f"Dice {dice_id} not found for update")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            logger.info(f"Updated Dice {dice_id} - {updated.name}")
            return updated

        except SQLAlchemyError:
            logger.exception(f"Database error while updating Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while updating dice."
            )
        except Exception:
            logger.exception(f"Unexpected error while updating Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while updating dice."
            )


    def delete_dice(
            self,
            dice_id: int):
        """Remove a dice by ID."""
        try:
            deleted = self.repo.delete(dice_id)
            if not deleted:
                logger.warning(f"Dice {dice_id} not found for deletion")
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            logger.info(f"Deleted Dice {dice_id} - {deleted}")
            return deleted
        except SQLAlchemyError:
            logger.exception(f"Database error while deleting Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while deleting dice."
            )
        except Exception:
            logger.exception(f"Unexpected error while deleting Dice {dice_id}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while deleting dice."
            )


    def _log_roll(
            self,
            user_id: int,
            campaign_id: int,
            class_id: int,
            diceset_id: int | None,
            name: str,
            result: int):
        """Log the dice data after a roll."""
        if not self.log_repo:
            logger.warning("DiceLogRepository not provided, skipping roll log")
            return
        try:
            log_entry = DiceLogCreate(
                user_id=user_id,
                campaign_id=campaign_id,
                class_id=class_id,
                diceset_id=diceset_id,
                roll=name,
                result=result,
                timestamp=datetime.now(timezone.utc)
            )
            self.log_repo.log_roll(log_entry)
            logger.info(f"Logged roll for Dice '{name}' by User {user_id}")
        except SQLAlchemyError:
            logger.exception("Database error while logging dice roll", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while logging dice roll."
            )
        except Exception:
            logger.exception("Unexpected error while logging dice roll", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while logging dice roll."
            )


    # Dice roll logic
    def roll_dice(
            self,
            dice_id: int,
            user_id: int,
            campaign_id: int,
            class_id: int,
    ):
        """Roll a dice (e.g. d6 -> random 1-6)
        and optionally log the result."""
        db_dice = self.repo.get_by_id(dice_id)
        if not db_dice:
            logger.warning(f"Dice {dice_id} not found for roll")
            raise HTTPException(
                status_code=404,
                detail=f"Dice with ID {dice_id} "
                       f"not found."
            )
        result = randint(1, db_dice.sides)
        logger.info(f"Rolled Dice {dice_id} - {db_dice.name}: {result}")

        if (user_id is not None
                and campaign_id is not None
                and class_id is not None):
            self._log_roll(
                user_id=user_id,
                campaign_id=campaign_id,
                class_id=class_id,
                diceset_id=None,
                name=db_dice.name,
                result=result
            )

        return DiceRollResult(
            id=db_dice.id,
            name=db_dice.name,
            sides=db_dice.sides,
            result=result
        )
