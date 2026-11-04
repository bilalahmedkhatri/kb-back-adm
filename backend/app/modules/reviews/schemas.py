import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class ReviewCreate(SQLModel):
    target_id: uuid.UUID
    target_type: str = Field(max_length=20)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(max_length=2000)


class ReviewPublic(SQLModel):
    id: uuid.UUID
    target_id: uuid.UUID
    target_type: str
    user_id: uuid.UUID | None = None
    rating: int
    reviewer_name: str
    comment: str
    created_at: datetime | None = None


class ReviewsPublic(SQLModel):
    data: list[ReviewPublic]
    count: int
