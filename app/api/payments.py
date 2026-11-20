from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse
)
from app.services import payment_service


router = APIRouter(
    prefix="/invoices/{invoice_id}/payments",
    tags=["Payments"]
)

@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)

def create_payment(
    invoice_id: int,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)

):

    return payment_service.create_payment(
        db=db,
        invoice_id=invoice_id,
        payment_data=payment_data
    )


@router.get(
    "",
    response_model=list[PaymentResponse]
)

def get_payments(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    return payment_service.get_payments(
        db=db,
        invoice_id=invoice_id
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)

def get_payment(
    invoice_id: int,
    payment_id: int,
    db: Session = Depends(get_db)
):

    return payment_service.get_payment(
        db=db,
        invoice_id=invoice_id,
        payment_id=payment_id
    )

@router.patch(
    "/{payment_id}",
    response_model=PaymentResponse
)

def update_payment(
    invoice_id: int,
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):

    return payment_service.update_payment(
        db=db,
        invoice_id=invoice_id,
        payment_id=payment_id,
        payment_data=payment_data
    )


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_payment(
    invoice_id: int,
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment_service.delete_payment(
        db=db,
        invoice_id=invoice_id,
        payment_id=payment_id
    )

    
