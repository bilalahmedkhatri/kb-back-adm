import uuid
from datetime import datetime
from typing import Any
from sqlmodel import Field, SQLModel


class PaymentTransactionCreate(SQLModel):
    order_id: uuid.UUID | None = None
    booking_id: uuid.UUID | None = None
    amount: float = Field(gt=0)
    currency: str = Field(default="AUD", max_length=10)
    provider: str = Field(max_length=50)
    payment_method_details: dict[str, Any] | None = None
    metadata_info: dict[str, Any] | None = None


class PaymentTransactionPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    order_id: uuid.UUID | None = None
    booking_id: uuid.UUID | None = None
    amount: float
    currency: str
    provider: str
    status: str
    transaction_reference: str | None = None
    refunded_amount: float
    failure_reason: str | None = None
    payment_method_details: dict[str, Any] | None = None
    metadata_info: dict[str, Any] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PaymentTransactionsPublic(SQLModel):
    data: list[PaymentTransactionPublic]
    count: int
