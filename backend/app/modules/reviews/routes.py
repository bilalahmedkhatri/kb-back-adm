import uuid
from typing import Any
from fastapi import APIRouter, Query
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.reviews.schemas import ReviewCreate, ReviewPublic, ReviewsPublic
from app.modules.reviews.service import create_review, get_reviews_by_target

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.post('/', response_model=ReviewPublic)
def create_new_review(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    review_in: ReviewCreate,
) -> Any:
    reviewer_name = current_user.full_name or current_user.email
    return create_review(session=session, review_in=review_in, reviewer_name=reviewer_name, user_id=current_user.id)


@router.get('/target/{target_id}', response_model=ReviewsPublic)
def read_reviews_for_target(
    target_id: uuid.UUID,
    session: SessionDep,
    target_type: str = Query(..., description='target type: product or stay'),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    reviews, count = get_reviews_by_target(
        session=session,
        target_id=target_id,
        target_type=target_type,
        skip=skip,
        limit=limit,
    )
    return ReviewsPublic(data=reviews, count=count)
