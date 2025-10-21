"""
dice_service.py

Business logic for dice handling.
"""
from random import randint
from datetime import datetime, timezone
from fastapi import HTTPException, Query
from typing import Annotated, List, Optional
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
                   offset: Annotated[int, Query(ge=0)] = 0,
                   limit: Annotated[int, Query(le=100)] = 100
                   ) -> List[DicePublic]:
        """Get a list of all dices."""
        return self.repo.list_all(offset, limit)


    def update_dice(self,
                    dice_id: int,
                    dice: DiceUpdate) -> Optional[DicePublic]:
        """Change the data from a dice."""
        return self.repo.update(dice_id, dice)


    def delete_dice(self, dice_id: int) -> bool:
        """Remove a dice by ID."""
        return self.repo.delete(dice_id)


    # Dice logic
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

        # Save result (optional if dice log is connected)
        if self.log_repo and user_id and campaign_id:
            log_entry = DiceLogCreate(
                user_id=user_id,
                campaign_id=campaign_id,
                roll=db_dice.name,
                result=result,
                timestamp=datetime.now(timezone.utc)
            )
            self.log_repo.add(log_entry)

        return DiceRollResult(
            id=db_dice.id,
            name=db_dice.name,
            sides=db_dice.sides,
            result=result
        )
