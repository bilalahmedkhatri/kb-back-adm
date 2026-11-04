import uuid
from typing import Any
from sqlmodel import Session, select, func
from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate, ProductUpdate


def create_product(*, session: Session, product_in: ProductCreate, vendor_id: uuid.UUID) -> Product:
    db_obj = Product.model_validate(product_in, update={'vendor_id': vendor_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_product_by_id(*, session: Session, product_id: uuid.UUID) -> Product | None:
    return session.get(Product, product_id)


def get_products(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 20,
    category: str | None = None,
    origin_island: str | None = None,
    status: str | None = None,
    vendor_id: uuid.UUID | None = None,
) -> tuple[list[Product], int]:
    query = select(Product)
    count_query = select(func.count()).select_from(Product)

    if category:
        query = query.where(Product.category == category)
        count_query = count_query.where(Product.category == category)
    if origin_island:
        query = query.where(Product.origin_island == origin_island)
        count_query = count_query.where(Product.origin_island == origin_island)
    if status:
        query = query.where(Product.status == status)
        count_query = count_query.where(Product.status == status)
    if vendor_id:
        query = query.where(Product.vendor_id == vendor_id)
        count_query = count_query.where(Product.vendor_id == vendor_id)

    total_count = session.exec(count_query).one()
    products = session.exec(query.offset(skip).limit(limit)).all()
    return list(products), total_count


def update_product(*, session: Session, db_product: Product, product_in: ProductUpdate) -> Product:
    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(*, session: Session, db_product: Product) -> None:
    session.delete(db_product)
    session.commit()
