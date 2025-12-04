"""
dice_service.py

Business logic for dice handling.
"""
import logging
from typing import List
from random import randint
from datetime import timezone

from models.schemas.dice_schema import *
from models.schemas.dicelog_schema import *
from repositories.dice_repository import DiceRepository
from repositories.dicelog_repository import DiceLogRepository
from services.dice.dice_service_exceptions import *



logger = logging.getLogger(__name__)


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
            logger.info(
                f"Created Dice {created.id} "
                f"- {created.name}"
            )
            return created

        except Exception:
            logger.exception(
                "Error while creating Dice",
                exc_info=True
            )
            raise DiceCreateError(
                "Error while creating dice."
            )


    def get_dice(self, dice_id: int) \
            -> Optional[DicePublic]:
        """Get the dice by ID."""
        try:
            db_dice = self.repo.get_by_id(dice_id)
            if not db_dice:
                logger.warning(
                    f"Dice {dice_id} not found"
                )
                raise DiceNotFoundError(
                    f"Dice with ID {dice_id} "
                    f"not found."
                )
            logger.info(
                f"Retrieved Dice {dice_id} "
                f"- {db_dice.name}"
            )
            return db_dice

        except Exception:
            logger.exception(
                f"Error while fetching "
                f"Dice {dice_id}",
                exc_info=True
            )
            raise DiceServiceError(
                "Error while fetching dice."
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
            logger.info(
                f"Listed {len(dices)} Dices "
                f"(offset={offset}, "
                f"limit={limit})"
            )
            return dices

        except Exception:
            logger.exception(
                "Error while listing Dices",
                exc_info=True
            )
            raise DiceServiceError(
                "Error while listing dices."
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
                logger.warning(
                    f"Dice {dice_id} "
                    f"not found for update"
                )
                raise DiceNotFoundError(
                    f"Dice with ID {dice_id} "
                    f"not found."
                )
            logger.info(
                f"Updated Dice {dice_id} "
                f"- {updated.name}"
            )
            return updated

        except Exception:
            logger.exception(
                f"Error while updating "
                f"Dice {dice_id}",
                exc_info=True
            )
            raise DiceServiceError(
                "Error while updating dice."
            )


    def delete_dice(
            self,
            dice_id: int):
        """Remove a dice by ID."""
        try:
            deleted = self.repo.delete(dice_id)
            if not deleted:
                logger.warning(
                    f"Dice {dice_id} not found "
                    f"for deletion"
                )
                raise DiceNotFoundError(
                    f"Dice with ID {dice_id} "
                    f"not found."
                )
            logger.info(
                f"Deleted Dice {dice_id} "
                f"- {deleted}"
            )
            return deleted

        except Exception:
            logger.exception(
                f"Error while deleting "
                f"Dice {dice_id}",
                exc_info=True
            )
            raise DiceServiceError(
                "Error while deleting dice."
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
            logger.warning(
                "DiceLogRepository not provided, "
                "skipping roll log")
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
            logger.info(
                f"Logged roll for Dice '{name}' "
                f"by User {user_id}"
            )
        except Exception:
            logger.exception(
                "Error while logging "
                "dice roll",
                exc_info=True
            )
            raise DiceServiceError(
                "Error while logging dice roll."
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
            logger.warning(
                f"Dice {dice_id} "
                f"not found for roll"
            )
            raise DiceNotFoundError(
                f"Dice with ID {dice_id} "
                f"not found."
            )
        result = randint(1, db_dice.sides)
        logger.info(
            f"Rolled Dice {dice_id} "
            f"- {db_dice.name}: {result}"
        )

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
