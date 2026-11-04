import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class VendorRegister(SQLModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    business_name: str = Field(max_length=255)
    business_description: str | None = Field(default=None, max_length=2000)
    contact_phone: str | None = Field(default=None, max_length=50)
    business_address: str | None = Field(default=None, max_length=500)


class VendorProfileUpdate(SQLModel):
    business_name: str | None = Field(default=None, max_length=255)
    business_description: str | None = Field(default=None, max_length=2000)
    contact_phone: str | None = Field(default=None, max_length=50)
    business_address: str | None = Field(default=None, max_length=500)


class VendorProfilePublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    business_name: str
    business_description: str | None = None
    contact_phone: str | None = None
    business_address: str | None = None
    verification_status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class VendorProfilesPublic(SQLModel):
    data: list[VendorProfilePublic]
    count: int


class VendorVerification(SQLModel):
    status: str
    notes: str | None = Field(default=None, max_length=1000)


class VendorStatsPublic(SQLModel):
    total_products: int
    active_products: int
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_revenue: float
