import uuid
from sqlmodel import Session, select, func
from app.modules.wishlist.models import WishlistItem
from app.modules.wishlist.schemas import WishlistItemCreate


def create_wishlist_item(*, session: Session, item_in: WishlistItemCreate, user_id: uuid.UUID) -> WishlistItem:
    # Check if already exists
    existing = session.exec(
        select(WishlistItem).where(
            WishlistItem.user_id == user_id,
            WishlistItem.target_id == item_in.target_id,
            WishlistItem.target_type == item_in.target_type,
        )
    ).first()
    if existing:
        return existing

    db_obj = WishlistItem.model_validate(item_in, update={"user_id": user_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_wishlist(*, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> tuple[list[WishlistItem], int]:
    query = select(WishlistItem).where(WishlistItem.user_id == user_id).order_by(WishlistItem.created_at.desc())
    count_query = select(func.count()).select_from(WishlistItem).where(WishlistItem.user_id == user_id)

    total_count = session.exec(count_query).one()
    items = session.exec(query.offset(skip).limit(limit)).all()
    return list(items), total_count


def delete_wishlist_item(*, session: Session, item_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    item = session.get(WishlistItem, item_id)
    if not item or item.user_id != user_id:
        return False
    session.delete(item)
    session.commit()
    return True
