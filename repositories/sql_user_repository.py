"""
sql_user_repository.py

Concrete implementation for sqlalchemy, user management.
"""
from sqlmodel import Session, select
from models.db_models.table_models import User
from models.schemas.user_schema import *
from repositories.user_repository import UserRepository
from auth.auth import hash_password
from typing import List, Optional
import logging



logger = logging.getLogger(__name__)


class SqlAlchemyUserRepository(UserRepository):
    """This dnd_class implement
    the user handling methods with sqlalchemy."""
    def __init__(self, session: Session):
        self.session = session
        logger.debug("SqlAlchemyUserRepository initialized")


    def get_by_id(self, user_id: int) \
            -> Optional[UserPublic]:
        """Method to get a user by ID."""
        db_user = self.session.get(User, user_id)
        if db_user:
            logger.debug(f"Retrieved User {user_id} - {db_user.user_name}")
            return UserPublic.model_validate(db_user)
        logger.debug(f"User {user_id} not found")
        return None


    def list_all(self,
                 offset: int = 0,
                 limit: int = 100,
                 name: Optional[str] = None
                 ) -> List[UserPublic]:
        """Method to show all users,
        optional filter by username."""
        query = select(User)
        if name:
            query = (
                query
                .where(User.user_name.ilike(f"%{name}%")))
        users = self.session.exec(
            query.offset(offset)
            .limit(limit)).all()
        logger.debug(f"Retrieved {len(users)} Users with filter name={name}")
        return [UserPublic.model_validate(u)
                for u in users]


    def add(self, user: UserCreate) \
            -> UserPublic:
        """Add a new user with hashed password."""
        db_user = User(
            user_name=user.user_name,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        logger.info(f"User added: {db_user.id} - {db_user.user_name}")
        return UserPublic.model_validate(db_user)


    def update(self,
               user_id: int,
               user: UserUpdate) \
            -> Optional[UserPublic]:
        """Method to update the data of a user."""
        db_user = self.session.get(User, user_id)
        if not db_user:
            logger.warning(f"Attempted to update non-existing User {user_id}")
            return None

        update_data = user.model_dump(exclude_unset=True)

        # If password changed -> hash the password
        if "password" in update_data:
            db_user.hashed_password = hash_password(update_data["password"])
            del update_data["password"]

        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        logger.info(f"Updated User {user_id} - {db_user.user_name}")
        return UserPublic.model_validate(db_user)


    def delete(self, user_id: int) \
            -> Optional[UserPublic]:
        """Method to remove a user."""
        db_user = self.session.get(User, user_id)
        if not db_user:
            logger.warning(f"Attempted to delete non-existing User {user_id}")
            return None
        self.session.delete(db_user)
        self.session.commit()
        logger.info(f"Deleted User {user_id} - {db_user.user_name}")
        return UserPublic.model_validate(db_user)


    def list_by_user(self, user_id: int) \
            -> List[UserPublic]:
        """Method to list by user."""
        db_users = (self.session.exec(
            select(User)
            .where(User.id == user_id))
                    .all())
        logger.debug(f"list_by_user called for user_id={user_id}, found {len(db_users)} users")
        return [UserPublic.model_validate(u)
                for u in db_users]
