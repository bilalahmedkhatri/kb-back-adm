import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class ProductCreate(SQLModel):
    name: str = Field(max_length=255)
    description: str = Field(max_length=2000)
    price: float = Field(gt=0)
    currency: str = Field(default='AUD', max_length=10)
    category: str = Field(max_length=100)
    origin_island: str = Field(max_length=100)
    material: str | None = Field(default=None, max_length=255)
    stock: int = Field(default=0, ge=0)
    images: list[str] = Field(default_factory=list)


class ProductUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    price: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, max_length=10)
    category: str | None = Field(default=None, max_length=100)
    origin_island: str | None = Field(default=None, max_length=100)
    material: str | None = Field(default=None, max_length=255)
    stock: int | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, max_length=20)
    images: list[str] | None = None


class ProductPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: str
    price: float
    currency: str
    category: str
    origin_island: str
    material: str | None = None
    stock: int
    status: str
    images: list[str]
    vendor_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int
