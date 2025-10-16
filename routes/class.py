"""
class.py

The API endpoints for classes.
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import SessionDep
from models.schemas.class_schema import *
from repositories.sql_class_repository import SqlAlchemyClassRepository
from services.class_service import ClassService


router = APIRouter(tags=["classes"])
