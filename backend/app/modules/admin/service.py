import uuid
from typing import Any
from sqlmodel import Session, func, select

from app.modules.users.models import User
from app.modules.vendors.models import VendorProfile
from app.modules.products.models import Product
from app.modules.stays.models import Stay
from app.modules.orders.models import Order
from app.modules.admin.models import AuditLog


def get_admin_stats(*, session: Session) -> dict[str, float | int]:
    total_users = session.exec(select(func.count()).select_from(User)).one()
    total_vendors = session.exec(select(func.count()).select_from(VendorProfile)).one()
    pending_vendors = session.exec(
        select(func.count()).select_from(VendorProfile).where(VendorProfile.verification_status == "pending")
    ).one()
    total_products = session.exec(select(func.count()).select_from(Product)).one()
    total_stays = session.exec(select(func.count()).select_from(Stay)).one()
    total_orders = session.exec(select(func.count()).select_from(Order)).one()

    total_revenue_val = session.exec(select(func.sum(Order.total))).one() or 0.0

    return {
        "total_users": total_users,
        "total_vendors": total_vendors,
        "pending_vendors": pending_vendors,
        "total_products": total_products,
        "total_stays": total_stays,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue_val),
    }


def create_audit_log(
    *,
    session: Session,
    user_id: uuid.UUID,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    details: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    session.add(log_entry)
    session.commit()
    session.refresh(log_entry)
    return log_entry


def get_audit_logs(*, session: Session, skip: int = 0, limit: int = 20) -> tuple[list[AuditLog], int]:
    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    count_query = select(func.count()).select_from(AuditLog)

    total_count = session.exec(count_query).one()
    logs = session.exec(query.offset(skip).limit(limit)).all()
    return list(logs), total_count
