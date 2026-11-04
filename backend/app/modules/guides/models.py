import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class Guide(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255, index=True)
    slug: str = Field(unique=True, index=True, max_length=255)
    excerpt: str = Field(max_length=500)
    content: str = Field(max_length=10000)
    image: str = Field(max_length=512)
    topic: str = Field(default="Culture & Heritage", max_length=100, index=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    author_name: str = Field(default="Kiribati Editorial Team", max_length=255)
    read_time: int = Field(default=5, ge=1)
    featured: bool = Field(default=False)
    published_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    author: Optional["User"] = Relationship()
