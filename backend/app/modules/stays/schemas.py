import uuid
from datetime import datetime
from typing import Any
from pydantic import field_validator
from sqlmodel import Field, SQLModel


class StayCreate(SQLModel):
    name: str = Field(max_length=255)
    description: str = Field(max_length=2000)
    price_per_night: float = Field(gt=0)
    currency: str = Field(default='AUD', max_length=10)
    type: str = Field(max_length=100)
    location: str = Field(max_length=255)
    island: str = Field(max_length=100)
    max_guests: int = Field(default=2, ge=1)
    bedrooms: int = Field(default=1, ge=0)
    beds: int = Field(default=1, ge=1)
    bathrooms: int = Field(default=1, ge=0)
    amenities: list[str] = Field(default_factory=list)
    eco_credentials: dict[str, Any] | None = None
    languages_spoken: list[str] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)


class StayUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    price_per_night: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, max_length=10)
    type: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    island: str | None = Field(default=None, max_length=100)
    max_guests: int | None = Field(default=None, ge=1)
    bedrooms: int | None = Field(default=None, ge=0)
    beds: int | None = Field(default=None, ge=1)
    bathrooms: int | None = Field(default=None, ge=0)
    amenities: list[str] | None = None
    eco_credentials: dict[str, Any] | None = None
    languages_spoken: list[str] | None = None
    status: str | None = Field(default=None, max_length=20)
    images: list[str] | None = None


class StayPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: str
    price_per_night: float
    currency: str
    type: str
    location: str
    island: str
    max_guests: int
    bedrooms: int
    beds: int
    bathrooms: int
    amenities: list[str] = Field(default_factory=list)
    eco_credentials: dict[str, Any] | None = None
    languages_spoken: list[str] = Field(default_factory=list)
    status: str
    images: list[str] = Field(default_factory=list)
    host_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("amenities", "images", "languages_spoken", mode="before")
    @classmethod
    def set_list_default(cls, v: Any) -> list[str]:
        if v is None:
            return []
        return v


class StaysPublic(SQLModel):
    data: list[StayPublic]
    count: int
