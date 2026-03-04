"""
ai_route.py

Endpoint for AI request.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from auth.auth import get_current_user
from rate_limit import limiter

router = APIRouter(tags=["ai_story"])
logger = logging.getLogger(__name__)