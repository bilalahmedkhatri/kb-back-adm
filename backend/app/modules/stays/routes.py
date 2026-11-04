import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.users.models import UserRole
from app.modules.stays.schemas import StayCreate, StayUpdate, StayPublic, StaysPublic
from app.modules.stays.service import (
    create_stay,
    get_stay_by_id,
    get_stays,
    update_stay,
    delete_stay,
)

router = APIRouter(prefix='/stays', tags=['stays'])


@router.get('/', response_model=StaysPublic)
def read_stays(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    island: str | None = Query(None),
    type: str | None = Query(None),
    status: str | None = Query(None),
    host_id: uuid.UUID | None = Query(None),
) -> Any:
    stays, count = get_stays(
        session=session,
        skip=skip,
        limit=limit,
        island=island,
        type=type,
        status=status,
        host_id=host_id,
    )
    return StaysPublic(data=stays, count=count)


@router.post('/', response_model=StayPublic)
def create_new_stay(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    stay_in: StayCreate,
) -> Any:
    if current_user.role not in (UserRole.VENDOR, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail='Only vendors/hosts or admins can create stays')
    return create_stay(session=session, stay_in=stay_in, host_id=current_user.id)


@router.get('/{stay_id}', response_model=StayPublic)
def read_stay_by_id(stay_id: str, session: SessionDep) -> Any:
    try:
        valid_uuid = uuid.UUID(stay_id)
    except ValueError:
        raise HTTPException(status_code=404, detail='Stay not found')
    stay = get_stay_by_id(session=session, stay_id=valid_uuid)
    if not stay:
        raise HTTPException(status_code=404, detail='Stay not found')
    return stay


@router.patch('/{stay_id}', response_model=StayPublic)
@router.put('/{stay_id}', response_model=StayPublic)
def update_stay_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    stay_id: uuid.UUID,
    stay_in: StayUpdate,
) -> Any:
    stay = get_stay_by_id(session=session, stay_id=stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail='Stay not found')
    if current_user.role != UserRole.ADMIN and current_user.id != stay.host_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return update_stay(session=session, db_stay=stay, stay_in=stay_in)


@router.delete('/{stay_id}')
def delete_stay_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    stay_id: uuid.UUID,
) -> Any:
    stay = get_stay_by_id(session=session, stay_id=stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail='Stay not found')
    if current_user.role != UserRole.ADMIN and current_user.id != stay.host_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    delete_stay(session=session, db_stay=stay)
    return {'message': 'Stay deleted successfully'}
