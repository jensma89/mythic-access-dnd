"""
sql_user_repository.py

Concrete implementation for sqlalchemy, user management.
"""
from fastapi import Query
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import User
from models.schemas.user_schema import *
from repositories.user_repository import UserRepository



class SqlAlchemyUserRepository(UserRepository):
    """This class implement
    the user handling methods with sqlalchemy."""
    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, user_id: int) -> Optional[UserPublic]:
        """Method to get a user by ID."""
        db_user = self.session.get(User, user_id)
        if db_user:
            return UserPublic.model_validate(db_user)
        return None


    def list_all(self,
                 offset: Annotated[int, Query(ge=0)] = 0,
                 limit: Annotated[int, Query(le=100)] = 100
                 ) -> List[UserPublic]:
        """Method to show all users."""
        users = self.session.exec(
            select(User)
            .offset(offset)
            .limit(limit)).all()
        return [UserPublic.model_validate(u) for u in users]


    def add(self, user: UserCreate) -> UserPublic:
        """Method to add a new user."""
        db_user = User(**user.model_dump())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserPublic.model_validate(db_user)


    def update(self,
               user_id: int,
               user: UserUpdate) -> Optional[UserPublic]:
        """Method to change the data of a user."""
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserPublic.model_validate(db_user)


    def delete(self, user_id: int) -> Optional[UserPublic]:
        """Method to remove a user."""
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None
        self.session.delete(db_user)
        self.session.commit()
        return UserPublic.model_validate(db_user)
