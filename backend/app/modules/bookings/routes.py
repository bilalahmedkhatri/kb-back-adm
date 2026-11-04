import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.users.models import UserRole
from app.modules.bookings.schemas import BookingCreate, BookingUpdateStatus, BookingPublic, BookingsPublic
from app.modules.bookings.service import (
    create_booking,
    get_booking_by_id,
    get_bookings,
    update_booking_status,
)
from app.modules.stays.service import get_stay_by_id

router = APIRouter(prefix='/bookings', tags=['bookings'])


@router.post('/', response_model=BookingPublic)
def create_new_booking(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    booking_in: BookingCreate,
) -> Any:
    stay = get_stay_by_id(session=session, stay_id=booking_in.stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail='Stay not found')
    return create_booking(session=session, booking_in=booking_in, user_id=current_user.id)


@router.get('/me', response_model=BookingsPublic)
def read_my_bookings(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    bookings, count = get_bookings(session=session, skip=skip, limit=limit, user_id=current_user.id)
    return BookingsPublic(data=bookings, count=count)


@router.get('/stay/{stay_id}', response_model=BookingsPublic)
def read_stay_bookings(
    stay_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    stay = get_stay_by_id(session=session, stay_id=stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail='Stay not found')
    if current_user.role != UserRole.ADMIN and current_user.id != stay.host_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    bookings, count = get_bookings(session=session, skip=skip, limit=limit, stay_id=stay_id)
    return BookingsPublic(data=bookings, count=count)


@router.get('/{booking_id}', response_model=BookingPublic)
def read_booking_by_id(
    booking_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    booking = get_booking_by_id(session=session, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    if current_user.role != UserRole.ADMIN and current_user.id != booking.user_id:
        stay = get_stay_by_id(session=session, stay_id=booking.stay_id)
        if not stay or stay.host_id != current_user.id:
            raise HTTPException(status_code=403, detail='Not enough permissions')
    return booking


@router.patch('/{booking_id}/status', response_model=BookingPublic)
def update_booking_status_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    booking_id: uuid.UUID,
    status_in: BookingUpdateStatus | None = None,
    status: str | None = Query(None),
) -> Any:
    booking = get_booking_by_id(session=session, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    stay = get_stay_by_id(session=session, stay_id=booking.stay_id)
    if current_user.role != UserRole.ADMIN and (not stay or stay.host_id != current_user.id):
        raise HTTPException(status_code=403, detail='Not enough permissions')

    effective_status = status_in or (BookingUpdateStatus(status=status) if status else None)
    if not effective_status:
        raise HTTPException(status_code=400, detail='Status is required')

    return update_booking_status(session=session, db_booking=booking, status_in=effective_status)
