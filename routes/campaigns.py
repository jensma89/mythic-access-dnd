"""
campaigns.py

The API routes for campaigns
"""
from typing import List, Annotated
from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from models.db_models.table_models import Campaign
from models.schemas.campaign_schema import *
from dependencies import SessionDep


router = APIRouter(tags=["campaigns"])
