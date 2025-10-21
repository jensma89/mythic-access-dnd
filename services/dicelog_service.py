"""
dicelog_service.py

Business logic for dice log handling.
"""
from random import randint
from datetime import datetime, timezone
from fastapi import HTTPException, Query
from typing import Annotated, List, Optional
from models.schemas.dicelog_schema import *
from repositories.dicelog_repository import DiceLogRepository



class