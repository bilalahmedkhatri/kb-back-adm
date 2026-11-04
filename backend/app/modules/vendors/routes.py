import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import settings
from app.modules.auth.deps import (
    get_current_admin,
    CurrentUser,
    SessionDep,
)
from app.modules.auth.models import Message
from app.modules.users.models import User, UserRole
from app.modules.users.schemas import UserCreate, UserPublic
from app.modules.users.service import create_user, get_user_by_email
from app.modules.vendors.schemas import (
    VendorProfilePublic,
    VendorProfileUpdate,
    VendorProfilesPublic,
    VendorRegister,
    VendorStatsPublic,
    VendorVerification,
)
from app.modules.vendors.service import (
    create_vendor_profile,
    get_vendor_profile_by_id,
    get_vendor_profile_by_user_id,
    get_vendor_profiles,
    get_vendor_stats,
    update_vendor_profile,
    verify_vendor,
)

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.post("/register", response_model=VendorProfilePublic)
def register_vendor(*, session: SessionDep, vendor_in: VendorRegister) -> Any:
    """
    Register as a vendor. Creates a user account with role=vendor
    and a VendorProfile with verification_status=pending.
    """
    existing_user = get_user_by_email(session=session, email=vendor_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists",
        )

    user_in = UserCreate(
        email=vendor_in.email,
        password=vendor_in.password,
        full_name=vendor_in.full_name,
        role=UserRole.VENDOR,
        is_active=True,
    )
    user = create_user(session=session, user_create=user_in)

    profile = create_vendor_profile(
        session=session, user_id=user.id, vendor_in=vendor_in
    )
    return profile


@router.get("/me", response_model=VendorProfilePublic)
def read_my_vendor_profile(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get own vendor profile.
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=403, detail="You are not registered as a vendor"
        )
    profile = get_vendor_profile_by_user_id(session=session, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Vendor profile not found")
    return profile


@router.get("/me/stats", response_model=VendorStatsPublic)
def read_my_vendor_stats(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get metrics & analytics summary for own vendor dashboard.
    """
    if current_user.role not in (UserRole.VENDOR, UserRole.ADMIN):
        raise HTTPException(
            status_code=403, detail="Vendor or admin access required"
        )
    return get_vendor_stats(session=session, vendor_id=current_user.id)


@router.patch("/me", response_model=VendorProfilePublic)
def update_my_vendor_profile(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    profile_in: VendorProfileUpdate,
) -> Any:
    """
    Update own vendor profile.
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=403, detail="You are not registered as a vendor"
        )
    profile = get_vendor_profile_by_user_id(session=session, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Vendor profile not found")
    return update_vendor_profile(session=session, profile=profile, profile_in=profile_in)


@router.get(
    "/",
    dependencies=[Depends(get_current_admin)],
    response_model=VendorProfilesPublic,
)
def read_vendors(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    status: str | None = Query(None, description="Filter by verification status"),
) -> Any:
    """
    List all vendor profiles. Admin only.
    """
    profiles, count = get_vendor_profiles(
        session=session, skip=skip, limit=limit, status=status
    )
    return VendorProfilesPublic(data=profiles, count=count)


@router.get(
    "/{profile_id}",
    response_model=VendorProfilePublic,
)
def read_vendor_profile(
    profile_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get a specific vendor profile.
    """
    profile = get_vendor_profile_by_id(session=session, profile_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Vendor profile not found")
    if current_user.role != UserRole.ADMIN and current_user.id != profile.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return profile


@router.patch(
    "/{profile_id}/verify",
    dependencies=[Depends(get_current_admin)],
    response_model=VendorProfilePublic,
)
def verify_vendor_profile(
    *,
    session: SessionDep,
    profile_id: uuid.UUID,
    verification: VendorVerification,
) -> Any:
    """
    Approve or reject a vendor profile. Admin only.
    """
    profile = get_vendor_profile_by_id(session=session, profile_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Vendor profile not found")
    return verify_vendor(
        session=session,
        profile=profile,
        status=verification.status,
        notes=verification.notes,
    )
