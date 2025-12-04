"""
diceset_service.py

Business logic for dice sets.
"""
from random import randint
from datetime import timezone

from repositories.dice_repository import *
from repositories.dicelog_repository import *
from repositories.sql_diceset_repository import *
from repositories.diceset_repository import *
from models.schemas.dicelog_schema import *
from services.diceset.diceset_service_exceptions import *
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
        try:
            # Validation max 5 sets per dnd dnd_class
            existing_sets = self.diceset_repo.get_by_class_id(
                diceset.class_id
            )
            logger.info(
                f"Creating DiceSet for Class {diceset.class_id}. "
                f"Existing sets: {len(existing_sets)}"
            )
            if len(existing_sets) >= 5:
                logger.warning(
                    f"Cannot create DiceSet for "
                    f"Class {diceset.class_id}: "
                    f"max 5 sets reached"
                )
                raise DiceSetCreateError(
                    "Maximum of 5 dice sets "
                    "per dnd_class reached."
                )

            # Check dice existence
            if self.dice_repo and diceset.dice_ids:
                for dice_id in diceset.dice_ids:
                    if not self.dice_repo.get_by_id(dice_id):
                        logger.warning(
                            f"Dice ID {dice_id} "
                            f"not found for new DiceSet"
                        )
                        raise DiceSetNotFoundError(
                            f"Dice {dice_id} not found."
                        )

            # Create the dice set
            created = self.diceset_repo.add(diceset)
            logger.info(
                f"Created DiceSet {created.id} "
                f"- {created.name} for "
                f"Class {diceset.class_id}"
            )

            # Count duplicates and persist quantities
            dice_count = {}
            if diceset.dice_ids:
                for d in diceset.dice_ids:
                    dice_count[d] = dice_count.get(d, 0) + 1
            if dice_count:
                self.diceset_repo.set_dice_quantities(
                    created.id, dice_count
                )
                logger.debug(
                    f"Stored dice quantities "
                    f"for DiceSet {created.id}: {dice_count}"
                )

            # Return fresh expanded object
            return self.diceset_repo.get_by_id(created.id)

        except Exception:
            logger.exception(
                "Error while creating DiceSet",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while creating dice set."
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
                logger.warning(
                    f"DiceSet {diceset_id} "
                    f"not found"
                )
                raise DiceSetNotFoundError(
                    f"Dice set with ID {diceset_id} "
                    f"not found."
                )
            logger.info(
                f"Retrieved DiceSet {diceset_id} "
                f"- {db_diceset.name}"
            )
            return db_diceset

        except Exception:
            logger.exception(
                f"Error while fetching "
                f"DiceSet {diceset_id}",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while fetching dice set."
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
                limit=limit
            )
        except Exception:
            logger.exception(
                "Error while listing DiceSets",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while listing dice sets."
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
                logger.warning(
                    f"DiceSet {diceset_id} "
                    f"not found for update"
                )
                raise DiceSetNotFoundError(
                    f"Dice set with ID {diceset_id} "
                    f"not found."
                )
            logger.info(
                f"Updated DiceSet {diceset_id} "
                f"- {updated.name}"
            )
            return updated

        except Exception:
            logger.exception(
                f"Error while updating "
                f"DiceSet {diceset_id}",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while updating dice set."
            )


    def delete_diceset(
            self,
            diceset_id: int) \
            -> Optional[DiceSetPublic]:
        """Remove a dnd_class and the belonging entries:
        dice sets and dice logs."""
        try:
            # Delete dice logs
            logs = (self.dicelog_repo
                    .list_by_diceset(diceset_id))
            for log in logs:
                self.dicelog_repo.delete(log.id)
                logger.info(
                    f"Deleted DiceLog {log.id} "
                    f"from DiceSet {diceset_id}"
                )

            # Finally delete diceset
            deleted = self.diceset_repo.delete(diceset_id)
            if not deleted:
                logger.warning(
                    f"DiceSet {diceset_id} "
                    f"not found for deletion"
                )
                raise DiceSetNotFoundError(
                    f"Dice set with ID {diceset_id} "
                    f"not found."
                )
            logger.info(
                f"Deleted DiceSet {diceset_id} "
                f"- {deleted.name}"
            )
            return deleted

        except Exception:
            logger.exception(
                f"Error while deleting "
                f"DiceSet {diceset_id}",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while deleting dice set."
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
            logger.warning(
                "DiceLogRepository not provided, "
                "skipping roll log"
            )
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
            logger.info(
                f"Logged DiceSet roll for "
                f"DiceSet {diceset_id} "
                f"by User {user_id}"
            )
        except Exception:
            logger.exception(
                f"Error while logging roll "
                f"for DiceSet {diceset_id}",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while logging dice set roll."
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
                       .get_orm_by_id(diceset_id))
            if not diceset or not diceset.dice_entries:
                logger.warning(
                    f"DiceSet {diceset_id} "
                    f"not found or has no dices"
                )
                raise DiceSetNotFoundError(
                    "Dice set not found or has no dices."
                )
            results = []
            total_sum = 0

            for dice_entry in diceset.dice_entries:
                dice = dice_entry.dice
                quantity = dice_entry.quantity

                for _ in range(quantity):
                    roll_value = randint(1, dice.sides)
                    results.append(DiceRollResult(
                        id=dice.id,
                        name=dice.name,
                        sides=dice.sides,
                        result=roll_value
                    ))
                    total_sum += roll_value

            logger.info(
                f"Rolled DiceSet {diceset_id} "
                f"by User {user_id}: "
                f"Results {[r.result for r in results]}, "
                f"Total: {total_sum}"
            )

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
        except Exception:
            logger.exception(
                f"Error while rolling "
                f"DiceSet {diceset_id}",
                exc_info=True
            )
            raise DiceSetServiceError(
                "Error while rolling dice set."
            )
