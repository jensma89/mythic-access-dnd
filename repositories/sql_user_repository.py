"""
sql_user_repository.py

Concrete SQL model for user management.
"""
from typing import List, Optional
from sqlmodel import Session, select
from models.db_models.table_models import User
from models.schemas.user_schema import UserCreate, UserUpdate, UserPublic
from user_repository import UserRepository



class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, user_id: int) -> Optional[UserPublic]:
        db_user = self.session.get(User, user_id)
        if db_user:
            return UserPublic.model_validate(db_user)
        return None


    def list_all(self,
                 offset: int = 0,
                 limit: int = 100) -> List[UserPublic]:
        users = self.session.exec(
            select(User)
            .offset(offset)
            .limit(limit)).all()
        return [UserPublic.model_validate(u) for u in users]


    def add(self, user: UserCreate) -> UserPublic:
        db_user = User(**user.model_dump())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserPublic.model_validate(db_user)


    def update(self,
               user_id: int,
               user: UserUpdate) -> Optional[UserPublic]:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserPublic.model_validate(db_user)


    def delete(self, user_id: int) -> bool:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return False
        self.session.delete(db_user)
        self.session.commit()
        return True
