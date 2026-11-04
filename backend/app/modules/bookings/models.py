import enum
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.stays.models import Stay


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class BookingStatus(str, enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'


class Booking(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, index=True)
    stay_id: uuid.UUID = Field(foreign_key='stay.id', nullable=False, index=True)
    check_in: datetime = Field(sa_type=DateTime(timezone=True))
    check_out: datetime = Field(sa_type=DateTime(timezone=True))
    guest_count: int = Field(default=1, ge=1)
    status: str = Field(default=BookingStatus.PENDING, max_length=20, index=True)
    message: str | None = Field(default=None, max_length=2000)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    user: 'User' = Relationship(back_populates='bookings')
    stay: 'Stay' = Relationship(back_populates='bookings')
