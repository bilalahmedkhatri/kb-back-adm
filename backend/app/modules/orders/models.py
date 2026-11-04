import enum
import uuid
from datetime import UTC, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.products.models import Product


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class OrderStatus(str, enum.Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, index=True)
    total: float = Field(ge=0)
    subtotal: float = Field(ge=0)
    delivery_fee: float = Field(default=15.0, ge=0)
    tax: float = Field(default=0.0, ge=0)
    currency: str = Field(default='AUD', max_length=10)
    status: str = Field(default=OrderStatus.PENDING, max_length=20, index=True)
    shipping_address: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    tracking_number: str | None = Field(default=None, max_length=255)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    user: 'User' = Relationship(back_populates='orders')
    items: list['OrderItem'] = Relationship(back_populates='order', cascade_delete=True)


class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key='order.id', nullable=False, index=True)
    product_id: uuid.UUID = Field(foreign_key='product.id', nullable=False, index=True)
    name: str = Field(max_length=255)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    image: str | None = Field(default=None, max_length=512)

    order: Order = Relationship(back_populates='items')
