from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.schemas.invoice_item import (
    InvoiceItemCreate,
    InvoiceItemUpdate
)



def get_editable_invoice(
        db: Session, 
        invoice_id: int
) -> Invoice:

    invoice = db.get(Invoice, invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    if invoice.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft invoices can have their items modified"
        )

    return invoice


def create_invoice_item(
        db: Session,
        invoice_id: int, 
        item_data: InvoiceItemCreate
):

    invoice = get_editable_invoice(db, invoice_id)

    db_item = InvoiceItem(
        invoice = invoice,
        **item_data.model_dump()
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_invoice_items(
    db: Session,
    invoice_id: int,
):

    invoice = db.get(Invoice, invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )


    db_items = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice_id
    ).all()

    return db_items


def get_invoice_item(
    db: Session,
    invoice_id: int,
    item_id: int
):

    invoice = db.get(Invoice, invoice_id)

    if invoice is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    db_item = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice.id,
        InvoiceItem.id == item_id
    ).first()

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )

    return db_item


def update_invoice_item(
    db: Session,
    invoice_id: int,
    item_id: int,
    item: InvoiceItemUpdate
):

    invoice = get_editable_invoice(db, invoice_id)

    db_item = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice.id,
        InvoiceItem.id == item_id
    ).first()

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )

    updated_data = item.model_dump(exclude_unset=True)

    for field in ("description", "quantity", "unit_price"):
        if field in updated_data and updated_data[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{field} cannot be NULL"
            )

    for key, value in updated_data.items():
        setattr(db_item, key, value)


    db.commit()
    db.refresh(db_item)

    return db_item


def delete_invoice_item(
    db: Session,
    invoice_id: int,
    item_id:int    
):

    invoice = get_editable_invoice(db, invoice_id)

    db_item = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice.id,
        InvoiceItem.id == item_id
    ).first()

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )


    db.delete(db_item)
    db.commit()



    