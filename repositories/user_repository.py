"""
user_repository.py

Defined methods for user management.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas.user_schema import *



class UserRepository(ABC):
    """This class defines the management methods for user"""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserPublic]:
        """Get user by id method"""
        pass


    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 100) -> List[UserPublic]:
        """Show all users method"""
        pass


    @abstractmethod
    def add(self, user: UserCreate) -> UserPublic:
        """Add new user method"""
        pass


    @abstractmethod
    def update(self, user_id: int, user: UserUpdate) -> Optional[UserPublic]:
        """Change user data method"""
        pass


    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Remove a user method"""
        pass
