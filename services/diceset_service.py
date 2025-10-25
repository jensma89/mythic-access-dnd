"""
diceset_service.py

Business logic for dice sets.
"""
from datetime import datetime, timezone
from random import randint
from fastapi import HTTPException
from typing import List, Optional
from models.schemas.diceset_schema import *
from repositories.diceset_repository import *
from repositories.dice_repository import *
from repositories.dicelog_repository import *
from models.schemas.dicelog_schema import *



class DiceSetService:
    """Business logic for dice set service."""

    def __init__(self,
                 dice_repo: DiceRepository,
                 diceset_repo: DiceSetRepository,
                 dicelog_repo: DiceLogRepository):
        self.dice_repo = dice_repo
        self.diceset_repo = diceset_repo
        self.dicelog_repo = dicelog_repo


    def create_diceset(self, diceset: DiceSetCreate) -> DiceSetPublic:
        """Create a new dice set (optionally with existing dice)."""

        # Validation max 5 sets per dnd class
        existing_sets = (self.diceset_repo
                         .get_by_class_id(diceset.class_id))
        if len(existing_sets) >= 5:
            raise HTTPException(status_code=400,
                                detail="Maximum of 5 dice sets "
                                       "per class reached.")

        # Check for existing dice IDs
        if self.dice_repo and diceset.dice_ids:
            for dice_id in diceset.dice_ids:
                if not self.dice_repo.get_by_id(dice_id):
                    raise HTTPException(status_code=404,
                                        detail=f"Dice {dice_id} not found.")
        return self.diceset_repo.add(diceset)


    def get_diceset(self, diceset_id: int) -> Optional[DiceSetPublic]:
        """Get a dice set by ID."""
        return self.diceset_repo.get_by_id(diceset_id)


    def list_dicesets(self,
                      offset: int = 0,
                      limit: int = 100
                      ) -> List[DiceSetPublic]:
        """Get a list of all dice sets."""
        return self.diceset_repo.list_all(offset=offset,
                                          limit=limit)


    def update_diceset(self,
                       diceset_id: int,
                       diceset: DiceSetUpdate) -> Optional[DiceSetPublic]:
        """Change data from a dice set."""
        return self.diceset_repo.update(diceset_id, diceset)


    def delete_diceset(self, diceset_id: int) -> bool:
        """Remove a class and the belonging entries:
        dice sets and dice logs."""

        # Delete dice logs
        logs = self.dicelog_repo.list_by_diceset(diceset_id)
        for log in logs:
            self.dicelog_repo.delete(log.id)

        # Finally delete diceset
        return self.diceset_repo.delete(diceset_id)


    def _log_roll(self,
                  user_id: int,
                  campaign_id: int,
                  class_id: int,
                  diceset_id: int,
                  name: str,
                  results: list,
                  total: int):
        """Function for dice set log entrys."""
        if not self.dicelog_repo:
            return
        log_entry = DiceLogCreate(
            user_id=user_id,
            campaign_id=campaign_id,
            class_id=class_id,
            diceset_id=diceset_id,
            roll=f"{name}: {[r.result for r in results]}",
            result=total,
            timestamp=datetime.now(timezone.utc)
        )
        self.dicelog_repo.add(log_entry)


    def roll_diceset(self,
                     user_id: int,
                     campaign_id: int,
                     class_id: int,
                     diceset_id: int):
        """Roll all dices in a set
        and return each result + total sum."""
        diceset = self.diceset_repo.get_by_id(diceset_id)
        if not diceset or not diceset.dices:
            raise HTTPException(status_code=404,
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

        self._log_roll(user_id,
                       campaign_id,
                       class_id,
                       diceset_id,
                       diceset.name,
                       results,
                       total_sum)

        return DiceSetRollResult(
            diceset_id=diceset.id,
            name=diceset.name,
            results=results,
            total=total_sum
        )
