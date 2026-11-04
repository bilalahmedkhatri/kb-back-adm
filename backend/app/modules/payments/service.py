import uuid
from sqlmodel import Session, select, func
from app.modules.payments.models import PaymentTransaction
from app.modules.payments.schemas import PaymentTransactionCreate


def create_payment_transaction(
    *, session: Session, tx_in: PaymentTransactionCreate, user_id: uuid.UUID
) -> PaymentTransaction:
    ref = f"TX-KB-{uuid.uuid4().hex[:8].upper()}"
    db_obj = PaymentTransaction.model_validate(
        tx_in,
        update={
            "user_id": user_id,
            "status": "succeeded",
            "transaction_reference": ref,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_payments(
    *, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20
) -> tuple[list[PaymentTransaction], int]:
    query = (
        select(PaymentTransaction)
        .where(PaymentTransaction.user_id == user_id)
        .order_by(PaymentTransaction.created_at.desc())
    )
    count_query = (
        select(func.count())
        .select_from(PaymentTransaction)
        .where(PaymentTransaction.user_id == user_id)
    )

    total_count = session.exec(count_query).one()
    txs = session.exec(query.offset(skip).limit(limit)).all()
    return list(txs), total_count
