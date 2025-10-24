"""
table_models.py

Table models for DB.
"""
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy import JSON, UniqueConstraint
from datetime import datetime, timezone
from typing import Dict, List, Optional



class User(SQLModel, table=True):
    """The table model for users."""
    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

    # Relationship to campaign
    campaigns: List["Campaign"] = Relationship(back_populates="creator")



class Campaign(SQLModel, table=True):
    """Model to create a campaigns table."""
    __table_args__ = (
        UniqueConstraint("title",
                         "created_by",
                         name="uq_user_title"),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    genre: str | None = None
    description: str | None = Field(default=None, description="Story of the campaign")
    max_classes: int
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ORM link to User
    creator: Optional[User] = Relationship(back_populates="campaigns")

    # Relationship to Class
    classes: List["Class"] = Relationship(back_populates="campaign")



class Class(SQLModel, table=True):
    """Table model for classes."""
    __table_args__ = (
        UniqueConstraint(
            "name",
            "campaign_id",
            name="uq_class_name_campaign"
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    race: str | None = None
    skills: Dict[str, int] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=lambda: {
            "Strength": 0,
            "Stamina": 0,
            "Dexterity": 0,
            "Intelligence": 0,
            "Charisma": 0

        }
    )
    notes: str | None = None
    inventory: str | None = None
    campaign_id: int = Field(foreign_key="campaign.id",
                             nullable=False,
                             index=True)

    # Link to Campaign
    campaign: "Campaign" = Relationship(back_populates="classes")

    # Link to DiceSet
    dice_sets: List["DiceSet"] = Relationship(back_populates="class_")


class DiceSetDice(SQLModel, table=True):
    """Table model for Dice to DiceSet relationships."""
    dice_set_id: int = Field(foreign_key="diceset.id", primary_key=True)
    dice_id: int = Field(foreign_key="dice.id", primary_key=True)


class DiceSet(SQLModel, table=True):
    """Table model for dice sets."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="Dice set", nullable=False)
    class_id: int = Field(foreign_key="class.id", nullable=False)
    campaign_id: int = Field(foreign_key="campaign.id", nullable=False)

    # Relationship to Class
    class_: "Class" = Relationship(back_populates="dice_sets")

    # Many-to-many relationship to Dice
    dices: List["Dice"] = Relationship(
        back_populates="dice_sets",
        link_model=DiceSetDice
    )


class Dice(SQLModel, table=True):
    """Different dices table model."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    sides: int

    # Many-to-many relationship to DiceSet
    dice_sets: List["DiceSet"] = Relationship(
        back_populates="dices",
        link_model=DiceSetDice
    )


class DiceLog(SQLModel, table=True):
    """Table model for dice logs."""
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    campaign_id: int = Field(foreign_key="campaign.id", nullable=False)
    diceset_id: int = Field(foreign_key="diceset.id", nullable=False)
    class_id: int = Field(foreign_key="diceset.id", nullable=False)
    roll: str = Field(nullable=False)
    result: int = Field(nullable=False)
