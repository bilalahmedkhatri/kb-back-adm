import enum
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class ListingStatus(str, enum.Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    REJECTED = 'rejected'


class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=2000)
    price: float = Field(gt=0)
    currency: str = Field(default='AUD', max_length=10)
    category: str = Field(max_length=100, index=True)
    origin_island: str = Field(max_length=100, index=True)
    material: str | None = Field(default=None, max_length=255)
    stock: int = Field(default=0, ge=0)
    status: str = Field(default=ListingStatus.PENDING, max_length=20, index=True)
    images: list[str] = Field(default_factory=list, sa_type=JSON)
    vendor_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, index=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    vendor: 'User' = Relationship(back_populates='products')
