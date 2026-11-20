from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.invoice import Invoice


def issue_invoice(
        db: Session, 
        invoice_id: int
):

    invoice = db.get(Invoice, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    if invoice.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft invoices can be issued"
        )

    if not invoice.items:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot issue invoice without items"
        )

    invoice.status = "unpaid"

    db.commit()
    db.refresh(invoice)

    return invoice