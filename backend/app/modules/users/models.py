import enum
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.products.models import Product
    from app.modules.stays.models import Stay
    from app.modules.orders.models import Order
    from app.modules.bookings.models import Booking
    from app.modules.reviews.models import Review
    from app.modules.conversations.models import Message
    from app.modules.wishlist.models import WishlistItem
    from app.modules.payments.models import PaymentTransaction


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    VENDOR = 'vendor'
    CUSTOMER = 'customer'


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    hashed_password: str
    role: str = Field(default=UserRole.CUSTOMER, max_length=20)
    phone: str | None = Field(default=None, max_length=50)
    whatsapp: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None, max_length=512)
    google_sub: str | None = Field(default=None, max_length=255)
    google_picture: str | None = Field(default=None, max_length=512)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    products: list['Product'] = Relationship(back_populates='vendor', cascade_delete=True)
    stays: list['Stay'] = Relationship(back_populates='host', cascade_delete=True)
    orders: list['Order'] = Relationship(back_populates='user', cascade_delete=True)
    bookings: list['Booking'] = Relationship(back_populates='user', cascade_delete=True)
    reviews: list['Review'] = Relationship(back_populates='user', cascade_delete=True)
    sent_messages: list['Message'] = Relationship(back_populates='sender', cascade_delete=True)
    wishlist_items: list['WishlistItem'] = Relationship(back_populates='user', cascade_delete=True)
    payments: list['PaymentTransaction'] = Relationship(back_populates='user', cascade_delete=True)
