import uuid
from sqlmodel import Session, select, func
from app.modules.reviews.models import Review
from app.modules.reviews.schemas import ReviewCreate


def create_review(*, session: Session, review_in: ReviewCreate, reviewer_name: str, user_id: uuid.UUID | None = None) -> Review:
    db_obj = Review.model_validate(review_in, update={'reviewer_name': reviewer_name, 'user_id': user_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_reviews_by_target(
    *,
    session: Session,
    target_id: uuid.UUID,
    target_type: str,
    skip: int = 0,
    limit: int = 20,
) -> tuple[list[Review], int]:
    query = select(Review).where(Review.target_id == target_id, Review.target_type == target_type)
    count_query = select(func.count()).select_from(Review).where(Review.target_id == target_id, Review.target_type == target_type)

    total_count = session.exec(count_query).one()
    reviews = session.exec(query.offset(skip).limit(limit)).all()
    return list(reviews), total_count
