
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,

)

def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
):
    transaction = Transaction(**transaction_data.model_dump())

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

@router.get(
    "",
    response_model=list[TransactionResponse],
)

def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.id.desc()).all()