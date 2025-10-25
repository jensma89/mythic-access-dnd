"""
dice_service.py

Business logic for dice handling.
"""
from random import randint
from datetime import datetime, timezone
from fastapi import HTTPException
from typing import List, Optional
from models.schemas.dice_schema import *
from models.schemas.dicelog_schema import *
from repositories.dice_repository import DiceRepository
from repositories.dicelog_repository import DiceLogRepository



class DiceService:
    """Business logic
    for dice service operations."""

    def __init__(self,
                 repository: DiceRepository,
                 log_repository: Optional[DiceLogRepository] = None):
        self.repo = repository
        self.log_repo = log_repository


    def create_dice(self, dice: DiceCreate) -> Optional[DicePublic]:
        """Create a new dice."""
        return self.repo.add(dice)


    def get_dice(self, dice_id: int) -> Optional[DicePublic]:
        """Get the dice by ID."""
        return self.repo.get_by_id(dice_id)


    def list_dices(self,
                   offset: int = 0,
                   limit: int = 100
                   ) -> List[DicePublic]:
        """Get a list of all dices."""
        return self.repo.list_all(offset=offset,
                                  limit=limit)


    def update_dice(self,
                    dice_id: int,
                    dice: DiceUpdate) -> Optional[DicePublic]:
        """Change the data from a dice."""
        return self.repo.update(dice_id, dice)


    def delete_dice(self, dice_id: int) -> bool:
        """Remove a dice by ID."""
        return self.repo.delete(dice_id)


    def _log_roll(self,
                  user_id: int,
                  campaign_id: int,
                  name: str,
                  result: int):
        """Log the dice data after a roll."""
        if not self.log_repo:
            return
        log_entry = DiceLogCreate(
            user_id=user_id,
            campaign_id=campaign_id,
            roll=name,
            result=result,
            timestamp=datetime.now(timezone.utc)
        )
        self.log_repo.add(log_entry)


    # Dice roll logic
    def roll_dice(self,
                  dice_id: int,
                  user_id: int | None = None,
                  campaign_id: int | None = None):
        """Roll a dice (e.g. d6 -> random 1-6)
        and optionally log the result."""
        db_dice = self.repo.get_by_id(dice_id)
        if not db_dice:
            raise HTTPException(status_code=404,
                                detail="Dice not found.")
        result = randint(1, db_dice.sides)

        if user_id and campaign_id:
            self._log_roll(user_id,
                           campaign_id,
                           db_dice.name,
                           result)

        return DiceRollResult(
            id=db_dice.id,
            name=db_dice.name,
            sides=db_dice.sides,
            result=result
        )
