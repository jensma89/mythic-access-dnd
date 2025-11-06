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



class DiceService:
    """Business logic
    for dice service operations."""

    def __init__(
            self,
            repository: DiceRepository,
            log_repository: Optional[DiceLogRepository] = None):
        self.repo = repository
        self.log_repo = log_repository


    def create_dice(self, dice: DiceCreate) \
            -> Optional[DicePublic]:
        """Create a new dice."""
        try:
            return self.repo.add(dice)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while creating dice."
            )
        except Exception:
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
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            return db_dice
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while fetching dice."
            )
        except Exception:
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
            return self.repo.list_all(
                offset=offset,
                limit=limit)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while listing dices."
            )
        except Exception:
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
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            return updated

        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while updating dice."
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error "
                       "while updating dice."
            )


    def delete_dice(
            self,
            dice_id: int) \
            -> Optional[DicePublic]:
        """Remove a dice by ID."""
        try:
            deleted = self.repo.delete(dice_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail=f"Dice with ID {dice_id} "
                           f"not found."
                )
            return deleted
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while deleting dice."
            )
        except Exception:
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
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error "
                       "while logging dice roll."
            )
        except Exception:
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
            raise HTTPException(
                status_code=404,
                detail=f"Dice with ID {dice_id} "
                       f"not found."
            )
        result = randint(1, db_dice.sides)

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
