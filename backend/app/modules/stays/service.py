import uuid
from sqlmodel import Session, select, func
from app.modules.stays.models import Stay
from app.modules.stays.schemas import StayCreate, StayUpdate


def create_stay(*, session: Session, stay_in: StayCreate, host_id: uuid.UUID) -> Stay:
    db_obj = Stay.model_validate(stay_in, update={'host_id': host_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_stay_by_id(*, session: Session, stay_id: uuid.UUID) -> Stay | None:
    return session.get(Stay, stay_id)


def get_stays(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 20,
    island: str | None = None,
    type: str | None = None,
    status: str | None = None,
    host_id: uuid.UUID | None = None,
) -> tuple[list[Stay], int]:
    query = select(Stay)
    count_query = select(func.count()).select_from(Stay)

    if island:
        query = query.where(Stay.island == island)
        count_query = count_query.where(Stay.island == island)
    if type:
        query = query.where(Stay.type == type)
        count_query = count_query.where(Stay.type == type)
    if status:
        query = query.where(Stay.status == status)
        count_query = count_query.where(Stay.status == status)
    if host_id:
        query = query.where(Stay.host_id == host_id)
        count_query = count_query.where(Stay.host_id == host_id)

    total_count = session.exec(count_query).one()
    stays = session.exec(query.offset(skip).limit(limit)).all()
    return list(stays), total_count


def update_stay(*, session: Session, db_stay: Stay, stay_in: StayUpdate) -> Stay:
    stay_data = stay_in.model_dump(exclude_unset=True)
    db_stay.sqlmodel_update(stay_data)
    session.add(db_stay)
    session.commit()
    session.refresh(db_stay)
    return db_stay


def delete_stay(*, session: Session, db_stay: Stay) -> None:
    session.delete(db_stay)
    session.commit()
