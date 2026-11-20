from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Literal
from fastapi import Query
from app.db.dependencies import get_db
from app.models.client import Client
from app.models.invoice import Invoice
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse
)
from app.services import invoice_service

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

@router.post(
    "",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED
)

def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):

    client = db.get(Client, invoice.client_id)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    #generate number from the sequence of postgre

    next_number = db.execute(
        text("SELECT nextval('invoice_number_seq')")
    ).scalar_one()

    invoice_number = f"INV-{next_number:06d}"

    db_invoice = Invoice(
        invoice_number=invoice_number,
        **invoice.model_dump()
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return db_invoice


@router.get(
    "",
    response_model=list[InvoiceResponse]
)

def get_invoices(
    db: Session = Depends(get_db),

    client_id: int | None = Query(default=None, gt=0),
    invoice_type: Literal["income", "expense"] | None = None,
    invoice_status: Literal[
        "draft",
        "unpaid",
        "partially_paid",
        "paid",
        "overdue",
        "cancelled"
    ] | None = None,

    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):

    query = db.query(Invoice)

    if client_id is not None:
        query = query.filter(Invoice.client_id == client_id)

    if invoice_type is not None:
        query = query.filter(Invoice.type == invoice_type)

    if invoice_status is not None:
        query = query.filter(Invoice.status == invoice_status)

    invoices = (
        query
        .order_by(Invoice.issue_date.desc(), Invoice.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return invoices


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse
)

def get_invoice_by_id(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    db_invoice = db.get(Invoice, invoice_id)

    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    return db_invoice


@router.patch(
    "/{invoice_id}",
    response_model=InvoiceResponse
)

def update_invoice(
    invoice_id: int,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db)
):

    db_invoice = db.get(Invoice, invoice_id)

    if db_invoice is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"

        )


    update_data = invoice.model_dump(exclude_unset=True)

    for field in ("client_id", "type", "issue_date", "due_date"):
        if field in update_data and update_data[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{field} cannot be NULL"

            )

    if "client_id" in update_data:

        client = db.get(Client, update_data["client_id"])

        if client is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )


    #verify new issue and due dates

    new_issue_date = update_data.get("issue_date", db_invoice.issue_date)

    new_due_date = update_data.get("due_date", db_invoice.due_date)

    if new_due_date < new_issue_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Due date cannot be earlier than Issue date"
        )

    for field, value in update_data.items():
            setattr(db_invoice, field, value)

    
    db.commit()
    db.refresh(db_invoice)

    return db_invoice


@router.post(
    "/{invoice_id}/cancel",
    response_model=InvoiceResponse
)

def cancel_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    db_invoice = db.get(Invoice, invoice_id)

    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    if db_invoice.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice is already cancelled"
        )

    if db_invoice.status not in ("draft", "unpaid"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft or unpaid invoices can be cancelled"
        )

    db_invoice.status = "cancelled"

    db.commit()
    db.refresh(db_invoice)

    return db_invoice


@router.post(
    "/{invoice_id}/issue",
    response_model=InvoiceResponse
)

def issue_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    return invoice_service.issue_invoice(db, invoice_id)

    