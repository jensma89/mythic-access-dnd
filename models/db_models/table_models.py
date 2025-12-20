"""
table_models.py

Table models for DB.
"""
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy import DateTime, JSON, Text, UniqueConstraint
from datetime import datetime, timezone
from typing import Dict, List, Optional



class User(SQLModel, table=True):
    """The table model for users."""
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.now(timezone.utc)
        )
    )

    # Relationship to campaign
    campaigns: List["Campaign"] = Relationship(
        back_populates="creator"
    )

    def __repr__(self):
        return (f"<User id={self.id} "
                f"user_name={self.user_name} "
                f"email={self.email}>")


class Campaign(SQLModel, table=True):
    """Model to create a campaigns table."""
    __tablename__ = "campaign"

    __table_args__ = (
        UniqueConstraint(
            "title",
            "created_by",
            name="uq_user_title"
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    genre: str | None = None
    description: str | None = Field(
        sa_column=Column(Text, nullable=True),
        default=None,
        description="Story of the campaign"
    )
    max_classes: int
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    # ORM link to User
    creator: Optional[User] = Relationship(
        back_populates="campaigns"
    )

    # Relationship to Class
    classes: List["Class"] = Relationship(
        back_populates="campaign"
    )

    def __repr__(self):
        return (
            f"<Campaign id={self.id} "
            f"title={self.title} "
            f"created_by={self.created_by}>"
        )


class Class(SQLModel, table=True):
    """Table model for dnd classes."""
    __tablename__ = "dnd_class"

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
    dnd_class: str
    skills: Dict[str, int] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=lambda: {
            "Constitution": 0,
            "Strength": 0,
            "Stamina": 0,
            "Dexterity": 0,
            "Wisdom": 0,
            "Intelligence": 0,
            "Charisma": 0

        }
    )
    notes: str | None = Field(sa_column=Column(Text, nullable=True))
    inventory: str | None = Field(sa_column=Column(Text, nullable=True))
    campaign_id: int = Field(
        foreign_key="campaign.id",
        nullable=False,
        index=True
    )
    user_id: int = Field(
        foreign_key="user.id",
        nullable=False,
        index=True
    )

    # Link to Campaign
    campaign: Optional["Campaign"] = Relationship(back_populates="classes")

    # Link to DiceSet
    dice_sets: List["DiceSet"] = Relationship(back_populates="dnd_class_")

    def __repr__(self):
        return f"<Class id={self.id} name={self.name} campaign_id={self.campaign_id}>"


class DiceSetDice(SQLModel, table=True):
    """Table model for Dice to DiceSet relationships."""

    dice_set_id: int = Field(foreign_key="diceset.id", primary_key=True)
    dice_id: int = Field(foreign_key="dice.id", primary_key=True)
    quantity: int = Field(default=1)

    diceset: Optional["DiceSet"] = Relationship(
        back_populates="dice_entries",
        sa_relationship_kwargs={"overlaps": "dices"}
    )

    dice: Optional["Dice"] = Relationship(
        back_populates="dice_entries",
        sa_relationship_kwargs={"overlaps": "dice_sets"}
    )


class DiceSet(SQLModel, table=True):
    """Table model for dice sets."""
    __tablename__ = "diceset"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="Dice set", nullable=False)
    dnd_class_id: int = Field(foreign_key="dnd_class.id", nullable=False)
    campaign_id: int = Field(foreign_key="campaign.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)

    dice_entries: List[DiceSetDice] = Relationship(back_populates="diceset")

    # Relationship to Class
    dnd_class_: Optional["Class"] = Relationship(back_populates="dice_sets")

    # Many-to-many relationship to Dice
    dices: List["Dice"] = Relationship(
        back_populates="dice_sets",
        link_model=DiceSetDice,
        sa_relationship_kwargs={"overlaps": "dice_entries,diceset,dice"}
    )

    def __repr__(self):
        return f"<DiceSet id={self.id} name={self.name} dnd_class_id={self.dnd_class_id}>"


class Dice(SQLModel, table=True):
    """Different dices table model."""
    __tablename__ = "dice"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    sides: int

    dice_entries: List[DiceSetDice] = Relationship(back_populates="dice")

    # Many-to-many relationship to DiceSet
    dice_sets: List["DiceSet"] = Relationship(
        back_populates="dices",
        link_model=DiceSetDice,
        sa_relationship_kwargs={"overlaps": "dice_entries,dice,diceset"}
    )


class DiceLog(SQLModel, table=True):
    """Table model for dice logs."""
    __tablename__ = "dicelog"

    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    campaign_id: int = Field(foreign_key="campaign.id", nullable=False)
    diceset_id: int | None = Field(foreign_key="diceset.id", nullable=True)
    dnd_class_id: int = Field(foreign_key="dnd_class.id", nullable=False)
    roll: str = Field(nullable=False)
    result: int = Field(nullable=False)

    def __repr__(self):
        return f"<DiceLog id={self.id} user_id={self.user_id} result={self.result}>"
