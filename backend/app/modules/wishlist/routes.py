import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.wishlist.schemas import WishlistItemCreate, WishlistItemPublic, WishlistPublic
from app.modules.wishlist.service import create_wishlist_item, get_user_wishlist, delete_wishlist_item

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get("/", response_model=WishlistPublic)
def read_my_wishlist(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    items, count = get_user_wishlist(session=session, user_id=current_user.id, skip=skip, limit=limit)
    return WishlistPublic(data=items, count=count)


@router.post("/", response_model=WishlistItemPublic)
def add_to_wishlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_in: WishlistItemCreate,
) -> Any:
    return create_wishlist_item(session=session, item_in=item_in, user_id=current_user.id)


@router.delete("/{item_id}")
def remove_from_wishlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_id: uuid.UUID,
) -> Any:
    success = delete_wishlist_item(session=session, item_id=item_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return {"message": "Wishlist item removed successfully"}
