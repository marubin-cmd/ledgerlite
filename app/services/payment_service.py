from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate


def get_total_paid(db: Session, invoice_id: int) -> Decimal:

    total_paid = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.invoice_id == invoice_id)
        .scalar()
    )

    return Decimal(total_paid)


def update_invoice_payment_status(db: Session, invoice: Invoice) -> None:

    total_paid = get_total_paid(db, invoice.id)

    if total_paid >= invoice.total:
        invoice.status = "paid"

    elif total_paid > 0:
        invoice.status = "partially_paid"

    else:
        invoice.status = "unpaid"


def create_payment(
    db: Session,
    invoice_id: int,
    payment_data: PaymentCreate
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    if invoice.status not in ("unpaid", "partially_paid"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payments can only be recorded for unpaid or partially paid invoices"
        )


    total_paid = get_total_paid(db, invoice_id)
    balance = invoice.total - total_paid

    if payment_data.amount > balance:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Payment amount exceeds the remaining balance"
        )

    
    payment = Payment(
        invoice_id = invoice_id,
        **payment_data.model_dump()
    )

    db.add(payment)
    db.flush()

    transaction = Transaction(
        description=f"Payment for {invoice.invoice_number}",
        amount = payment.amount,
        transaction_type = invoice.type,
        transaction_date = payment.payment_date,
        payment_id = payment.id
    )

    db.add(transaction)

    update_invoice_payment_status(db, invoice)

    db.commit()
    db.refresh(payment)

    return payment


def get_payments(
    db: Session, 
    invoice_id: int
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    payments = db.query(Payment).filter(
        Payment.invoice_id == invoice_id
        ).order_by(Payment.payment_date.desc(), Payment.id.desc()).all()

    return payments


def get_payment(
    db: Session,
    invoice_id: int,
    payment_id: int
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    payment = db.query(Payment).filter(
        Payment.invoice_id == invoice_id,
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment
    

def update_payment(
    db: Session,
    invoice_id: int,
    payment_id: int,
    payment_data: PaymentUpdate
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    payment = db.query(Payment).filter(
        Payment.invoice_id == invoice_id,
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    updated_data = payment_data.model_dump(exclude_unset = True)

    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    for field in ("amount", "payment_date", "payment_method"):
        if field in updated_data and updated_data[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{field} cannot be null"
            )

    new_amount = updated_data.get("amount", payment.amount)

    total_paid = get_total_paid(db, invoice_id)

    new_total_paid = total_paid - payment.amount + new_amount

    if new_total_paid > invoice.total:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Updated payment would exceed the invoice balance"
        )

    for field, value in updated_data.items():
        setattr(payment, field, value)

    db.flush()

    transaction = payment.transaction

    if transaction:
        transaction.amount = payment.amount
        transaction.transaction_date = payment.payment_date

    update_invoice_payment_status(db, invoice)

    db.commit()
    db.refresh(payment)

    return payment

def delete_payment(
    db: Session,
    invoice_id: int,
    payment_id: int
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    payment = db.query(Payment).filter(
        Payment.invoice_id == invoice_id,
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )


    db.delete(payment)

    db.flush()

    update_invoice_payment_status(db, invoice)

    db.commit()
    

