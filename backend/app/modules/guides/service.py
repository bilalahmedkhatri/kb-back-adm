import uuid
import re
from sqlmodel import Session, select, func
from app.modules.guides.models import Guide
from app.modules.guides.schemas import GuideCreate, GuideUpdate


def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug[:200]


def create_guide(*, session: Session, guide_in: GuideCreate, author_id: uuid.UUID, author_name: str) -> Guide:
    base_slug = guide_in.slug or slugify(guide_in.title)
    unique_slug = base_slug
    counter = 1
    while session.exec(select(Guide).where(Guide.slug == unique_slug)).first():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    db_obj = Guide.model_validate(
        guide_in,
        update={
            "slug": unique_slug,
            "author_id": author_id,
            "author_name": author_name,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_guide_by_id_or_slug(*, session: Session, id_or_slug: str) -> Guide | None:
    try:
        guid = uuid.UUID(id_or_slug)
        guide = session.get(Guide, guid)
        if guide:
            return guide
    except ValueError:
        pass
    return session.exec(select(Guide).where(Guide.slug == id_or_slug)).first()


def get_guides(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 20,
    topic: str | None = None,
    featured: bool | None = None,
) -> tuple[list[Guide], int]:
    query = select(Guide).order_by(Guide.published_at.desc())
    count_query = select(func.count()).select_from(Guide)

    if topic:
        query = query.where(Guide.topic == topic)
        count_query = count_query.where(Guide.topic == topic)
    if featured is not None:
        query = query.where(Guide.featured == featured)
        count_query = count_query.where(Guide.featured == featured)

    total_count = session.exec(count_query).one()
    guides = session.exec(query.offset(skip).limit(limit)).all()
    return list(guides), total_count


def update_guide(*, session: Session, db_guide: Guide, guide_in: GuideUpdate) -> Guide:
    update_data = guide_in.model_dump(exclude_unset=True)
    if "title" in update_data and "slug" not in update_data:
        update_data["slug"] = slugify(update_data["title"])
    db_guide.sqlmodel_update(update_data)
    session.add(db_guide)
    session.commit()
    session.refresh(db_guide)
    return db_guide


def delete_guide(*, session: Session, db_guide: Guide) -> None:
    session.delete(db_guide)
    session.commit()
