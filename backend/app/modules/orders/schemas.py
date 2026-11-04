import uuid
from datetime import datetime
from typing import Any
from sqlmodel import Field, SQLModel


class OrderItemCreate(SQLModel):
    product_id: uuid.UUID
    name: str = Field(max_length=255)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    image: str | None = Field(default=None, max_length=512)


class OrderItemPublic(SQLModel):
    id: uuid.UUID
    product_id: uuid.UUID
    name: str
    price: float
    quantity: int
    image: str | None = None


class OrderCreate(SQLModel):
    subtotal: float = Field(default=0.0, ge=0)
    delivery_fee: float = Field(default=15.0, ge=0)
    tax: float = Field(default=0.0, ge=0)
    total: float = Field(default=0.0, ge=0)
    currency: str = Field(default='AUD', max_length=10)
    shipping_address: dict[str, Any]
    items: list[OrderItemCreate]


class OrderUpdateStatus(SQLModel):
    status: str = Field(max_length=20)
    tracking_number: str | None = Field(default=None, max_length=255)


class OrderPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total: float
    subtotal: float
    delivery_fee: float
    tax: float
    currency: str
    status: str
    shipping_address: dict[str, Any]
    tracking_number: str | None = None
    items: list[OrderItemPublic]
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int
