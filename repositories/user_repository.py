"""
user_repository.py

Interface for user management.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas.user_schema import *



class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserPublic]:
        pass


    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 100) -> List[UserPublic]:
        pass


    @abstractmethod
    def add(self, user: UserCreate) -> UserPublic:
        pass


    @abstractmethod
    def update(self, user_id: int, user: UserUpdate) -> Optional[UserPublic]:
        pass


    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass