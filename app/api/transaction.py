
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)
from datetime import date

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
    response_model=list[TransactionResponse]
)

def list_transactions(
    transaction_type: str | None = Query(
        default=None,
        pattern="^(income|expense)$"   
    ),
    start_date: date | None = None,
    end_date: date | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):  

    query = db.query(Transaction)

    if transaction_type is not None:

        query = query.filter(
            Transaction.transaction_type == transaction_type
        )

    if start_date is not None:

        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:

        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    return (

        query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
        .offset(skip)
        .limit(limit)
        .all()

    )


@router.put(
    "/{transaction_id}",
    response_model= TransactionResponse,
)

def update_transaction(
    transaction_id: int,
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
):

    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    for field, value in transaction_data.model_dump().items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction



@router.delete(
    "/{transaction_id}",
    status_code= status.HTTP_204_NO_CONTENT,
)

def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Transaction not found",
        )

    db.delete(transaction)
    db.commit()


@router.get("/summary")
def get_transaction_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if start_date is not None:
        query = query.filter(Transaction.transaction_date >= start_date)

    if end_date is not None:
        query = query.filter(Transaction.transaction_date <= end_date)

    total_income, total_expenses = query.with_entities(
        func.coalesce(
            func.sum(
                case(
                    (Transaction.transaction_type == "income", Transaction.amount),
                    else_=0,
                )
            ),
            0,
        ),
        func.coalesce(
            func.sum(
                case(
                    (Transaction.transaction_type == "expense", Transaction.amount),
                    else_=0,
                )
            ),
            0,
        ),
    ).one()

    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
    }
