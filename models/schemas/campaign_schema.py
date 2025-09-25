"""
campaign_schema.py

Request/response schemas for campaigns.
"""
from sqlmodel import SQLModel


class CampaignBase(SQLModel):
    """Base Campaign model that shares common definitions"""
    title: str
    genre: str
    description: str
    max_classes: int


class CampaignCreate(SQLModel):





class Campaign(SQLModel, table=True):
    """Model to create a campaign table."""
    __table_args__ = (
        UniqueConstraint("title",
                         "created_by",
                         name="uq_user_title"),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str
    genre: str | None = None
    description: str | None = Field(default=None, description="Story of the campaign")
    max_classes: int
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ORM link to User
    creator: Optional[User] = Relationship(back_populates="campaigns")