import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class WishlistItemCreate(SQLModel):
    target_id: uuid.UUID
    target_type: str = Field(max_length=20)


class WishlistItemPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    target_id: uuid.UUID
    target_type: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WishlistPublic(SQLModel):
    data: list[WishlistItemPublic]
    count: int
