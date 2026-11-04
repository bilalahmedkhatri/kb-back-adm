import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class Review(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    target_id: uuid.UUID = Field(index=True)
    target_type: str = Field(max_length=20, index=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key='user.id', nullable=True, index=True)
    rating: int = Field(ge=1, le=5)
    reviewer_name: str = Field(max_length=255)
    comment: str = Field(max_length=2000)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    user: Optional['User'] = Relationship(back_populates='reviews')
