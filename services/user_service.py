"""
user_service.py

Business logic for user.
"""
from typing import List, Optional
from models.schemas.user_schema import UserCreate, UserUpdate, UserPublic
from repositories.user_repository import UserRepository



class UserService:
    """Initialise the bussines logic for user service operations."""
    def __init__(self, repository: UserRepository):
        self.repo = repository


    def create_user(self, user: UserCreate) -> UserPublic:
        """Create a new user."""
        return self.repo.add(user)


    def get_user(self, user_id: int) -> Optional[UserPublic]:
        """Get a user by id."""
        return self.repo.get_by_id(user_id)


    def list_users(self,
                   offset: int = 0,
                   limit: int = 100) -> List[UserPublic]:
        """Get a list of all users."""
        return self.repo.list_all(offset, limit)


    def update_user(self,
                    user_id: int,
                    user: UserUpdate) -> Optional[UserPublic]:
        """Make changes by a user."""
        return self.repo.update(user_id, user)


    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        return self.repo.delete(user_id)
