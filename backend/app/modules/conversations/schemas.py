import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class MessageCreate(SQLModel):
    text: str = Field(max_length=2000)


class MessagePublic(SQLModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    sender_id: uuid.UUID
    text: str
    timestamp: datetime | None = None


class MessagesPublic(SQLModel):
    data: list[MessagePublic]
    count: int


class ConversationCreate(SQLModel):
    vendor_id: uuid.UUID | None = None
    participant_names: list[str] = Field(default_factory=list)
    initial_message: str | None = Field(default=None, max_length=2000)


class ConversationPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID | None = None
    vendor_id: uuid.UUID | None = None
    participant_names: list[str]
    last_message: str | None = None
    last_message_time: datetime | None = None
    unread: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ConversationsPublic(SQLModel):
    data: list[ConversationPublic]
    count: int
