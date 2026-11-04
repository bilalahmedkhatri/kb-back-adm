import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.users.models import UserRole
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductPublic, ProductsPublic
from app.modules.products.service import (
    create_product,
    get_product_by_id,
    get_products,
    update_product,
    delete_product,
)

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', response_model=ProductsPublic)
def read_products(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    category: str | None = Query(None),
    origin_island: str | None = Query(None),
    island: str | None = Query(None),
    status: str | None = Query(None),
    vendor_id: uuid.UUID | None = Query(None),
) -> Any:
    effective_island = origin_island or island
    products, count = get_products(
        session=session,
        skip=skip,
        limit=limit,
        category=category,
        origin_island=effective_island,
        status=status,
        vendor_id=vendor_id,
    )
    return ProductsPublic(data=products, count=count)


@router.post('/', response_model=ProductPublic)
def create_new_product(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    product_in: ProductCreate,
) -> Any:
    if current_user.role not in (UserRole.VENDOR, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail='Only vendors or admins can create products')
    return create_product(session=session, product_in=product_in, vendor_id=current_user.id)


@router.get('/{product_id}', response_model=ProductPublic)
def read_product_by_id(product_id: str, session: SessionDep) -> Any:
    try:
        valid_uuid = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail='Product not found')
    product = get_product_by_id(session=session, product_id=valid_uuid)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@router.patch('/{product_id}', response_model=ProductPublic)
@router.put('/{product_id}', response_model=ProductPublic)
def update_product_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    product_id: uuid.UUID,
    product_in: ProductUpdate,
) -> Any:
    product = get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    if current_user.role != UserRole.ADMIN and current_user.id != product.vendor_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return update_product(session=session, db_product=product, product_in=product_in)


@router.delete('/{product_id}')
def delete_product_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    product_id: uuid.UUID,
) -> Any:
    product = get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    if current_user.role != UserRole.ADMIN and current_user.id != product.vendor_id:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    delete_product(session=session, db_product=product)
    return {'message': 'Product deleted successfully'}
