"""
sql_dicelog_repository.py

Concrete implementation for sqlalchemy, campaign management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import DiceLog
from models.schemas.dicelog_schema import *
from repositories.dicelog_repository import DiceLogRepository



class SqlAlchemyDiceLogRepository:
    """This class implement
    the dice log handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, dicelog_id: int) -> Optional[DiceLogPublic]:
        """Method to get a dice log by ID."""
        db_dicelog = self.session.get(DiceLog, dicelog_id)
        if db_dicelog:
            return DiceLogPublic.model_validate(db_dicelog)
        return None


    def add(self, log: DiceLogCreate) -> DiceLogPublic:
        """Method to create a new dice log."""
        db_dicelog = DiceLog(**log.dict())
        self.session.add(db_dicelog)
        self.session.commit()
        self.session.refresh(db_dicelog)

        # FIFO cleanup delete oldest if bigger than 100
        logs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.user_id == log.user_id)
            .order_by(DiceLog.timestamp.desc())
        ).all()

        if len(logs) > 100:
            # Delete oldest, keep 100 newest
            for old_log in logs[100:]:
                self.session.delete(old_log)
            self.session.commit()
        return DiceLogPublic.model_validate(db_dicelog)


    def list_logs(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 100
    ) -> List[DiceLogPublic]:
        """List logs by user."""
        dicelogs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.user_id == user_id)
            .order_by(DiceLog.timestamp.desc())
            .offset(offset)
            .limit(limit)
        ).all()
        return [DiceLogPublic.model_validate(d) for d in dicelogs]
