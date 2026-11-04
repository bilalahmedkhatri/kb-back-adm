import uuid
from typing import Any
from fastapi import APIRouter, HTTPException
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.conversations.schemas import (
    ConversationCreate,
    ConversationPublic,
    ConversationsPublic,
    MessageCreate,
    MessagePublic,
    MessagesPublic,
)
from app.modules.conversations.service import (
    create_conversation,
    create_message,
    get_conversation_by_id,
    get_conversations,
    get_messages_for_conversation,
)

router = APIRouter(prefix='/conversations', tags=['conversations'])


@router.post('/', response_model=ConversationPublic)
def create_new_conversation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conv_in: ConversationCreate,
) -> Any:
    return create_conversation(session=session, conv_in=conv_in, sender_id=current_user.id)


@router.get('/', response_model=ConversationsPublic)
def read_conversations(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    convs, count = get_conversations(session=session, user_id=current_user.id, skip=skip, limit=limit)
    return ConversationsPublic(data=convs, count=count)


@router.get('/{conversation_id}', response_model=ConversationPublic)
def read_conversation_by_id(
    conversation_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    conv = get_conversation_by_id(session=session, conversation_id=conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return conv


@router.get('/{conversation_id}/messages', response_model=MessagesPublic)
def read_conversation_messages(
    conversation_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    conv = get_conversation_by_id(session=session, conversation_id=conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')
    msgs, count = get_messages_for_conversation(
        session=session, conversation_id=conversation_id, skip=skip, limit=limit
    )
    return MessagesPublic(data=msgs, count=count)


@router.post('/{conversation_id}/messages', response_model=MessagePublic)
def send_message(
    *,
    conversation_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    msg_in: MessageCreate,
) -> Any:
    conv = get_conversation_by_id(session=session, conversation_id=conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return create_message(
        session=session, conversation_id=conversation_id, sender_id=current_user.id, msg_in=msg_in
    )
