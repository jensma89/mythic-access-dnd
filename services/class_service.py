"""
class_service.py

Business logic for classes.
"""
from fastapi import Query
from typing import List, Optional, Annotated
from models.schemas.class_schema import *
from repositories.class_repository import ClassRepository

# Todo next: class service, class api endpoints


class ClassService:
    """Initialise the bussines logic
    for class service operations."""
    def __init__(self, repository: ClassRepository):
        self.repo = repository


    def create(self, new_class: ClassCreate) -> ClassPublic:
        """Create a new class."""
        pass

    # get class, list classes, update class, delete class