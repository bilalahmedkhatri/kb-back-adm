from typing import Any
from fastapi import APIRouter
from app.modules.auth.deps import SessionDep, CurrentUser
from app.modules.payments.schemas import (
    PaymentTransactionCreate,
    PaymentTransactionPublic,
    PaymentTransactionsPublic,
)
from app.modules.payments.service import create_payment_transaction, get_user_payments

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/me", response_model=PaymentTransactionsPublic)
def read_my_payments(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    txs, count = get_user_payments(session=session, user_id=current_user.id, skip=skip, limit=limit)
    return PaymentTransactionsPublic(data=txs, count=count)


@router.post("/intent", response_model=PaymentTransactionPublic)
def create_payment_intent(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    tx_in: PaymentTransactionCreate,
) -> Any:
    return create_payment_transaction(session=session, tx_in=tx_in, user_id=current_user.id)
