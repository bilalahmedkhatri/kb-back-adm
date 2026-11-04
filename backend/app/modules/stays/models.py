import enum
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.bookings.models import Booking


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class Stay(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=2000)
    price_per_night: float = Field(gt=0)
    currency: str = Field(default='AUD', max_length=10)
    type: str = Field(max_length=100, index=True)
    location: str = Field(max_length=255)
    island: str = Field(max_length=100, index=True)
    max_guests: int = Field(default=2, ge=1)
    bedrooms: int = Field(default=1, ge=0)
    beds: int = Field(default=1, ge=1)
    bathrooms: int = Field(default=1, ge=0)
    amenities: list[str] = Field(default_factory=list, sa_type=JSON)
    eco_credentials: dict[str, Any] | None = Field(default=None, sa_type=JSON)
    languages_spoken: list[str] | None = Field(default=None, sa_type=JSON)
    status: str = Field(default='pending', max_length=20, index=True)
    images: list[str] = Field(default_factory=list, sa_type=JSON)
    host_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, index=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    host: 'User' = Relationship(back_populates='stays')
    bookings: list['Booking'] = Relationship(back_populates='stay', cascade_delete=True)
