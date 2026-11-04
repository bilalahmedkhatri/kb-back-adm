import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.users.models import UserRole
from app.modules.orders.schemas import OrderCreate, OrderUpdateStatus, OrderPublic, OrdersPublic
from app.modules.orders.service import (
    create_order,
    get_order_by_id,
    get_orders,
    get_vendor_orders,
    update_order_status,
)

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/', response_model=OrderPublic)
def create_new_order(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    order_in: OrderCreate,
) -> Any:
    return create_order(session=session, order_in=order_in, user_id=current_user.id)


@router.get('/me', response_model=OrdersPublic)
def read_my_orders(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    orders, count = get_orders(session=session, skip=skip, limit=limit, user_id=current_user.id)
    return OrdersPublic(data=orders, count=count)


@router.get('/vendor', response_model=OrdersPublic)
def read_vendor_orders(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
    status: str | None = Query(None),
) -> Any:
    if current_user.role not in (UserRole.VENDOR, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail='Vendor or admin access required')
    orders, count = get_vendor_orders(
        session=session, vendor_id=current_user.id, skip=skip, limit=limit, status=status
    )
    return OrdersPublic(data=orders, count=count)


@router.get('/', response_model=OrdersPublic)
def read_all_orders(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
    status: str | None = Query(None),
) -> Any:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail='Admin privileges required')
    orders, count = get_orders(session=session, skip=skip, limit=limit, status=status)
    return OrdersPublic(data=orders, count=count)


@router.get('/{order_id}', response_model=OrderPublic)
def read_order_by_id(
    order_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    order = get_order_by_id(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if current_user.role != UserRole.ADMIN and current_user.id != order.user_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return order


@router.patch('/{order_id}/status', response_model=OrderPublic)
def update_order_status_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    order_id: uuid.UUID,
    status_in: OrderUpdateStatus | None = None,
    status: str | None = Query(None),
) -> Any:
    order = get_order_by_id(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if current_user.role not in (UserRole.ADMIN, UserRole.VENDOR):
        raise HTTPException(status_code=403, detail='Not enough permissions')
    
    effective_status = status_in or (OrderUpdateStatus(status=status) if status else None)
    if not effective_status:
        raise HTTPException(status_code=400, detail='Status is required')

    return update_order_status(session=session, db_order=order, status_in=effective_status)
