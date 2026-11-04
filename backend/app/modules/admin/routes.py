from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.modules.auth.deps import CurrentUser, SessionDep
from app.modules.users.models import UserRole
from app.modules.admin.schemas import AdminStatsPublic, AuditLogsPublic
from app.modules.admin.service import get_admin_stats, get_audit_logs

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsPublic)
def read_admin_stats(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get system-wide overview statistics for admin dashboard. Admin only.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Admin privileges required"
        )
    return get_admin_stats(session=session)


@router.get("/audit-logs", response_model=AuditLogsPublic)
def read_audit_logs(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    """
    Get audit log history of platform actions. Admin only.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Admin privileges required"
        )
    logs, count = get_audit_logs(session=session, skip=skip, limit=limit)
    return AuditLogsPublic(data=logs, count=count)
