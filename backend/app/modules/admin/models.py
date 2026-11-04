import uuid
from datetime import UTC, datetime
from typing import Any
from sqlalchemy import DateTime, JSON
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class AuditLog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    action: str = Field(max_length=100, index=True)
    resource_type: str = Field(max_length=50, index=True)
    resource_id: str | None = Field(default=None, max_length=255)
    details: dict[str, Any] | None = Field(default=None, sa_type=JSON)
    ip_address: str | None = Field(default=None, max_length=100)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
