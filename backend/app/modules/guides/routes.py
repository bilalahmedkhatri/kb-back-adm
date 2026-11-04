import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.users.models import UserRole
from app.modules.guides.schemas import GuideCreate, GuidePublic, GuidesPublic, GuideUpdate
from app.modules.guides.service import (
    create_guide,
    delete_guide,
    get_guide_by_id_or_slug,
    get_guides,
    update_guide,
)

router = APIRouter(prefix="/guides", tags=["guides"])


@router.get("/", response_model=GuidesPublic)
def read_guides(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    topic: str | None = Query(None),
    featured: bool | None = Query(None),
) -> Any:
    guides, count = get_guides(session=session, skip=skip, limit=limit, topic=topic, featured=featured)
    return GuidesPublic(data=guides, count=count)


@router.get("/{id_or_slug}", response_model=GuidePublic)
def read_guide_by_id_or_slug(id_or_slug: str, session: SessionDep) -> Any:
    guide = get_guide_by_id_or_slug(session=session, id_or_slug=id_or_slug)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide article not found")
    return guide


@router.post("/", response_model=GuidePublic)
def create_new_guide(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    guide_in: GuideCreate,
) -> Any:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can publish editorial guides")
    author_name = current_user.full_name or "Kiribati Editorial Team"
    return create_guide(session=session, guide_in=guide_in, author_id=current_user.id, author_name=author_name)


@router.patch("/{guide_id}", response_model=GuidePublic)
def update_guide_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    guide_id: uuid.UUID,
    guide_in: GuideUpdate,
) -> Any:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can edit editorial guides")
    guide = get_guide_by_id_or_slug(session=session, id_or_slug=str(guide_id))
    if not guide:
        raise HTTPException(status_code=404, detail="Guide article not found")
    return update_guide(session=session, db_guide=guide, guide_in=guide_in)


@router.delete("/{guide_id}")
def delete_guide_by_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    guide_id: uuid.UUID,
) -> Any:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete editorial guides")
    guide = get_guide_by_id_or_slug(session=session, id_or_slug=str(guide_id))
    if not guide:
        raise HTTPException(status_code=404, detail="Guide article not found")
    delete_guide(session=session, db_guide=guide)
    return {"message": "Guide article deleted successfully"}
