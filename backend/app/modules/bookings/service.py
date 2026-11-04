import uuid
from sqlmodel import Session, select, func
from app.modules.bookings.models import Booking
from app.modules.bookings.schemas import BookingCreate, BookingUpdateStatus


def create_booking(*, session: Session, booking_in: BookingCreate, user_id: uuid.UUID) -> Booking:
    db_obj = Booking.model_validate(booking_in, update={'user_id': user_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_booking_by_id(*, session: Session, booking_id: uuid.UUID) -> Booking | None:
    return session.get(Booking, booking_id)


def get_bookings(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 20,
    user_id: uuid.UUID | None = None,
    stay_id: uuid.UUID | None = None,
    status: str | None = None,
) -> tuple[list[Booking], int]:
    query = select(Booking)
    count_query = select(func.count()).select_from(Booking)

    if user_id:
        query = query.where(Booking.user_id == user_id)
        count_query = count_query.where(Booking.user_id == user_id)
    if stay_id:
        query = query.where(Booking.stay_id == stay_id)
        count_query = count_query.where(Booking.stay_id == stay_id)
    if status:
        query = query.where(Booking.status == status)
        count_query = count_query.where(Booking.status == status)

    total_count = session.exec(count_query).one()
    bookings = session.exec(query.offset(skip).limit(limit)).all()
    return list(bookings), total_count


def update_booking_status(*, session: Session, db_booking: Booking, status_in: BookingUpdateStatus) -> Booking:
    db_booking.status = status_in.status
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)
    return db_booking
