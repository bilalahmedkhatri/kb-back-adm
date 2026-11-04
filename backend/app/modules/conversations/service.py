import uuid
from sqlmodel import Session, select, func, or_
from app.modules.conversations.models import Conversation, Message
from app.modules.conversations.schemas import ConversationCreate, MessageCreate
from datetime import UTC, datetime


def create_conversation(*, session: Session, conv_in: ConversationCreate, sender_id: uuid.UUID) -> Conversation:
    conv = Conversation(
        user_id=sender_id,
        vendor_id=conv_in.vendor_id,
        participant_names=conv_in.participant_names,
        last_message=conv_in.initial_message,
        last_message_time=datetime.now(UTC),
        unread=True,
    )
    session.add(conv)
    session.commit()
    session.refresh(conv)

    if conv_in.initial_message:
        msg = Message(
            conversation_id=conv.id,
            sender_id=sender_id,
            text=conv_in.initial_message,
            timestamp=datetime.now(UTC),
        )
        session.add(msg)
        session.commit()
        session.refresh(conv)

    return conv


def get_conversation_by_id(*, session: Session, conversation_id: uuid.UUID) -> Conversation | None:
    return session.get(Conversation, conversation_id)


def get_conversations(
    *, session: Session, user_id: uuid.UUID | None = None, skip: int = 0, limit: int = 20
) -> tuple[list[Conversation], int]:
    query = select(Conversation).order_by(Conversation.last_message_time.desc())
    count_query = select(func.count()).select_from(Conversation)

    if user_id:
        filter_stmt = or_(Conversation.user_id == user_id, Conversation.vendor_id == user_id)
        query = query.where(filter_stmt)
        count_query = count_query.where(filter_stmt)

    total_count = session.exec(count_query).one()
    convs = session.exec(query.offset(skip).limit(limit)).all()
    return list(convs), total_count


def create_message(*, session: Session, conversation_id: uuid.UUID, sender_id: uuid.UUID, msg_in: MessageCreate) -> Message:
    conv = session.get(Conversation, conversation_id)
    now = datetime.now(UTC)
    
    msg = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        text=msg_in.text,
        timestamp=now,
    )
    session.add(msg)

    if conv:
        conv.last_message = msg_in.text
        conv.last_message_time = now
        conv.unread = True
        session.add(conv)

    session.commit()
    session.refresh(msg)
    return msg


def get_messages_for_conversation(
    *, session: Session, conversation_id: uuid.UUID, skip: int = 0, limit: int = 20
) -> tuple[list[Message], int]:
    query = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
    count_query = select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)

    total_count = session.exec(count_query).one()
    msgs = session.exec(query.offset(skip).limit(limit)).all()
    return list(msgs), total_count
