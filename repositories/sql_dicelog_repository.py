"""
sql_dicelog_repository.py

Concrete implementation for sqlalchemy, campaign management.
"""
from typing import List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import DiceLog
from models.schemas.dicelog_schema import *
from repositories.dicelog_repository import DiceLogRepository



class SqlAlchemyDiceLogRepository(DiceLogRepository):
    """This class implement
    the dice log handling methods with sqlalchemy."""

    def __init__(self, session: Session):
        self.session = session


    def list_by_user(self, user_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific user."""
        dicelogs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.user_id == user_id)
        ).all()
        return [DiceLogPublic.model_validate(l)
                for l in dicelogs]


    def list_by_campaign(self, campaign_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific campaign."""
        dicelogs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.campaign_id == campaign_id)
        ).all()
        return [DiceLogPublic.model_validate(l)
                for l in dicelogs]


    def list_by_class(self, class_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific DnD class."""
        dicelogs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.class_id == class_id)
        ).all()
        return [DiceLogPublic.model_validate(d)
                for d in dicelogs]


    def list_by_diceset(self, diceset_id: int) \
            -> List[DiceLogPublic]:
        """List all dice logs belonging to a specific dice set."""
        dicelogs = self.session.exec(
            select(DiceLog)
            .where(DiceLog.diceset_id == diceset_id)
        ).all()
        return [DiceLogPublic.model_validate(log)
                for log in dicelogs]


    def get_by_id(self, dicelog_id: int) \
            -> Optional[DiceLogPublic]:
        """Method to get a dice log by ID."""
        db_dicelog = self.session.get(DiceLog, dicelog_id)
        if db_dicelog:
            return DiceLogPublic.model_validate(db_dicelog)
        return None


    def add(self, log: DiceLogCreate) \
            -> DiceLogPublic:
        """Method to create a new dice log."""
        db_dicelog = DiceLog(**log.model_dump())
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


    def delete(self, dicelog_id: int) \
            -> Optional[DiceLogPublic]:
        """Delete a dice log by ID."""
        db_dicelog = self.session.get(DiceLog, dicelog_id)
        if not db_dicelog:
            return None
        self.session.delete(db_dicelog)
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
        return [DiceLogPublic.model_validate(d)
                for d in dicelogs]


    def log_roll(self, log: DiceLogCreate) -> DiceLogPublic:
        """Method for services to store dice rolls."""
        return self.add(log)
