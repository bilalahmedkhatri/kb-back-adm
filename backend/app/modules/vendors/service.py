import uuid

from sqlmodel import Session, select

from app.modules.vendors.models import VendorProfile
from app.modules.vendors.schemas import VendorRegister, VendorProfileUpdate


def create_vendor_profile(
    *, session: Session, user_id: uuid.UUID, vendor_in: VendorRegister
) -> VendorProfile:
    db_obj = VendorProfile.model_validate(
        vendor_in,
        update={"user_id": user_id, "verification_status": "pending"},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_vendor_profile_by_user_id(
    *, session: Session, user_id: uuid.UUID
) -> VendorProfile | None:
    statement = select(VendorProfile).where(VendorProfile.user_id == user_id)
    return session.exec(statement).first()


def get_vendor_profile_by_id(
    *, session: Session, profile_id: uuid.UUID
) -> VendorProfile | None:
    return session.get(VendorProfile, profile_id)


def update_vendor_profile(
    *, session: Session, profile: VendorProfile, profile_in: VendorProfileUpdate
) -> VendorProfile:
    update_data = profile_in.model_dump(exclude_unset=True)
    profile.sqlmodel_update(update_data)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def verify_vendor(
    *, session: Session, profile: VendorProfile, status: str, notes: str | None = None
) -> VendorProfile:
    profile.verification_status = status
    if notes is not None:
        profile.verification_notes = notes
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def get_vendor_profiles(
    *, session: Session, skip: int = 0, limit: int = 20, status: str | None = None
) -> tuple[list[VendorProfile], int]:
    statement = select(VendorProfile)
    if status:
        statement = statement.where(VendorProfile.verification_status == status)
    count = len(session.exec(statement).all())
    statement = statement.offset(skip).limit(limit)
    profiles = session.exec(statement).all()
    return list(profiles), count


def get_vendor_stats(*, session: Session, vendor_id: uuid.UUID) -> dict[str, float | int]:
    from sqlmodel import func
    from app.modules.products.models import Product
    from app.modules.orders.models import Order, OrderItem

    # Products stats
    total_products = session.exec(
        select(func.count()).select_from(Product).where(Product.vendor_id == vendor_id)
    ).one()

    active_products = session.exec(
        select(func.count()).select_from(Product).where(
            Product.vendor_id == vendor_id, Product.status == 'active'
        )
    ).one()

    # Vendor orders stats via order items
    subquery = select(OrderItem.order_id).join(Product, OrderItem.product_id == Product.id).where(Product.vendor_id == vendor_id)

    total_orders = session.exec(
        select(func.count(func.distinct(Order.id))).where(Order.id.in_(subquery))
    ).one()

    pending_orders = session.exec(
        select(func.count(func.distinct(Order.id))).where(
            Order.id.in_(subquery), Order.status == 'pending'
        )
    ).one()

    completed_orders = session.exec(
        select(func.count(func.distinct(Order.id))).where(
            Order.id.in_(subquery), Order.status.in_(['delivered', 'shipped', 'confirmed'])
        )
    ).one()

    # Revenue sum from vendor's order items
    rev_statement = select(func.sum(OrderItem.price * OrderItem.quantity)).join(
        Product, OrderItem.product_id == Product.id
    ).where(Product.vendor_id == vendor_id)
    
    total_revenue = session.exec(rev_statement).one() or 0.0

    return {
        "total_products": total_products,
        "active_products": active_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": float(total_revenue),
    }

