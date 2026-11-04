import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class BookingCreate(SQLModel):
    stay_id: uuid.UUID
    check_in: datetime
    check_out: datetime
    guest_count: int = Field(default=1, ge=1)
    message: str | None = Field(default=None, max_length=2000)


class BookingUpdateStatus(SQLModel):
    status: str = Field(max_length=20)


class BookingPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    stay_id: uuid.UUID
    check_in: datetime
    check_out: datetime
    guest_count: int
    status: str
    message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BookingsPublic(SQLModel):
    data: list[BookingPublic]
    count: int
