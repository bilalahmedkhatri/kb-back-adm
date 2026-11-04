import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key='user.id', nullable=True, index=True)
    vendor_id: uuid.UUID | None = Field(default=None, foreign_key='user.id', nullable=True, index=True)
    participant_names: list[str] = Field(default_factory=list, sa_type=JSON)
    last_message: str | None = Field(default=None, max_length=2000)
    last_message_time: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    unread: bool = Field(default=False)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    messages: list['Message'] = Relationship(back_populates='conversation', cascade_delete=True)
    user: Optional['User'] = Relationship(sa_relationship_kwargs={'foreign_keys': '[Conversation.user_id]'})
    vendor: Optional['User'] = Relationship(sa_relationship_kwargs={'foreign_keys': '[Conversation.vendor_id]'})


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key='conversation.id', nullable=False, index=True)
    sender_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, index=True)
    text: str = Field(max_length=2000)
    timestamp: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    conversation: Conversation = Relationship(back_populates='messages')
    sender: 'User' = Relationship(back_populates='sent_messages')
