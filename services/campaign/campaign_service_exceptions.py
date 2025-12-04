"""
campaign_service_exceptions.py

Custom exceptions for campaign services.
"""


class CampaignServiceError(Exception):
    """Base exception for CampaignService errors."""
    pass


class CampaignNotFoundError(Exception):
    """Raised when a campaign is not found."""
    pass


class CampaignCreateError(Exception):
    """Raised when creating a campaign fails."""
    pass


class CampaignUpdateError(Exception):
    """Raised when updating a campaign fails."""
    pass


class CampaignDeleteError(Exception):
    """Raised when deleting a campaign fails"""
    pass
