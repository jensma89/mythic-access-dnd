"""
campaign_schema.py

Request/response schemas for campaigns.
"""
from sqlmodel import SQLModel
from datetime import datetime



class CampaignBase(SQLModel):
    """Base Campaign model that shares common definitions."""
    title: str
    genre: str
    description: str
    max_classes: int


class CampaignCreate(CampaignBase):
    """Fields to create a campaign."""
    created_by: int


class CampaignUpdate(SQLModel):
    """Fields to update a campaign."""
    title: str | None = None
    genre: str | None = None
    description: str | None = None


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
