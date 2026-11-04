import uuid
from sqlmodel import Session, select, func
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.schemas import OrderCreate, OrderUpdateStatus


def create_order(*, session: Session, order_in: OrderCreate, user_id: uuid.UUID) -> Order:
    computed_subtotal = order_in.subtotal if order_in.subtotal > 0 else sum(i.price * i.quantity for i in order_in.items)
    computed_total = order_in.total if order_in.total > 0 else (computed_subtotal + order_in.delivery_fee + order_in.tax)

    db_order = Order(
        user_id=user_id,
        subtotal=computed_subtotal,
        delivery_fee=order_in.delivery_fee,
        tax=order_in.tax,
        total=computed_total,
        currency=order_in.currency,
        shipping_address=order_in.shipping_address,
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    for item in order_in.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            name=item.name,
            price=item.price,
            quantity=item.quantity,
            image=item.image,
        )
        session.add(db_item)
    
    session.commit()
    session.refresh(db_order)
    return db_order


def get_order_by_id(*, session: Session, order_id: uuid.UUID) -> Order | None:
    return session.get(Order, order_id)


def get_orders(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 20,
    user_id: uuid.UUID | None = None,
    status: str | None = None,
) -> tuple[list[Order], int]:
    query = select(Order)
    count_query = select(func.count()).select_from(Order)

    if user_id:
        query = query.where(Order.user_id == user_id)
        count_query = count_query.where(Order.user_id == user_id)
    if status:
        query = query.where(Order.status == status)
        count_query = count_query.where(Order.status == status)

    total_count = session.exec(count_query).one()
    orders = session.exec(query.offset(skip).limit(limit)).all()
    return list(orders), total_count


def update_order_status(*, session: Session, db_order: Order, status_in: OrderUpdateStatus) -> Order:
    db_order.status = status_in.status
    if status_in.tracking_number is not None:
        db_order.tracking_number = status_in.tracking_number
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


def get_vendor_orders(
    *,
    session: Session,
    vendor_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
    status: str | None = None,
) -> tuple[list[Order], int]:
    from app.modules.products.models import Product

    subquery = select(OrderItem.order_id).join(Product, OrderItem.product_id == Product.id).where(Product.vendor_id == vendor_id)
    
    query = select(Order).where(Order.id.in_(subquery))
    count_query = select(func.count(func.distinct(Order.id))).where(Order.id.in_(subquery))

    if status:
        query = query.where(Order.status == status)
        count_query = count_query.where(Order.status == status)

    total_count = session.exec(count_query).one()
    orders = session.exec(query.offset(skip).limit(limit)).all()
    return list(orders), total_count

