import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Optional
from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class PaymentTransaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    order_id: uuid.UUID | None = Field(default=None, foreign_key="order.id", nullable=True, index=True)
    booking_id: uuid.UUID | None = Field(default=None, foreign_key="booking.id", nullable=True, index=True)
    amount: float = Field(gt=0)
    currency: str = Field(default="AUD", max_length=10)
    provider: str = Field(max_length=50)  # 'stripe', 'paypal', 'cash_on_delivery'
    status: str = Field(default="succeeded", max_length=20)  # 'pending', 'succeeded', 'failed', 'refunded'
    transaction_reference: str | None = Field(default=None, max_length=255)
    refunded_amount: float = Field(default=0.0, ge=0)
    failure_reason: str | None = Field(default=None, max_length=500)
    payment_method_details: dict[str, Any] | None = Field(default=None, sa_type=JSON)
    metadata_info: dict[str, Any] | None = Field(default=None, sa_type=JSON)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    user: Optional["User"] = Relationship(back_populates="payments")
