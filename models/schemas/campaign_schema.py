"""
campaign_schema.py

Request/response schemas for campaigns.
"""
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional



class CampaignBase(SQLModel):
    """Base Campaign model that shares common definitions."""
    title: str
    genre: str
    description: str
    max_classes: int


class CampaignCreateInput(SQLModel):
    title: str
    genre: str
    description: str
    max_classes: int


class CampaignCreate(CampaignBase):
    """Fields to create a campaign."""
    created_by: Optional[int] = None

    def set_user(self, user_id: int):
        self.created_by = user_id


class CampaignUpdate(SQLModel):
    """Fields to update a campaign."""
    title: Optional[str] = None
    genre: Optional[str] =  None
    description: Optional[str] = None


class CampaignPublic(CampaignBase):
    """Model to respond public data."""
    id: int
    created_by: int
    created_at: datetime

    class Config:
        """Formatted timestamp"""
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
