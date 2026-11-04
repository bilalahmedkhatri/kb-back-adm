import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class GuideCreate(SQLModel):
    title: str = Field(max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    excerpt: str = Field(max_length=500)
    content: str = Field(max_length=10000)
    image: str = Field(max_length=512)
    topic: str = Field(default="Culture & Heritage", max_length=100)
    read_time: int = Field(default=5, ge=1)
    featured: bool = Field(default=False)


class GuideUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str | None = Field(default=None, max_length=10000)
    image: str | None = Field(default=None, max_length=512)
    topic: str | None = Field(default=None, max_length=100)
    read_time: int | None = Field(default=None, ge=1)
    featured: bool | None = None


class GuidePublic(SQLModel):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str
    content: str
    image: str
    topic: str
    author_id: uuid.UUID
    author_name: str
    read_time: int
    featured: bool
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class GuidesPublic(SQLModel):
    data: list[GuidePublic]
    count: int
