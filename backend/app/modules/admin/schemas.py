import uuid
from datetime import datetime
from typing import Any
from sqlmodel import SQLModel


class AdminStatsPublic(SQLModel):
    total_users: int
    total_vendors: int
    pending_vendors: int
    total_products: int
    total_stays: int
    total_orders: int
    total_revenue: float


class AuditLogPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    action: str
    resource_type: str
    resource_id: str | None = None
    details: dict[str, Any] | None = None
    ip_address: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuditLogsPublic(SQLModel):
    data: list[AuditLogPublic]
    count: int
