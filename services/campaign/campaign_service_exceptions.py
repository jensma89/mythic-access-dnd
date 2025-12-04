"""
campaign_service_exceptions.py

Custom exceptions for campaign services.
"""


class CampaignServiceError(Exception):
    """Base exception for CampaignService errors."""
    pass


class CampaignNotFoundError(CampaignServiceError):
    """Raised when a campaign is not found."""
    pass


class CampaignCreateError(CampaignServiceError):
    """Raised when creating a campaign fails."""
    pass


class CampaignUpdateError(CampaignServiceError):
    """Raised when updating a campaign fails."""
    pass


class CampaignDeleteError(CampaignServiceError):
    """Raised when deleting a campaign fails"""
    pass
