from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.invoice_item import (
    InvoiceItemCreate,
    InvoiceItemUpdate,
    InvoiceItemResponse
)
from app.services import invoice_item_service


router = APIRouter(
    prefix="/invoices/{invoice_id}/items",
    tags=["Invoice Items"]
)


@router.post(
    "",
    response_model=InvoiceItemResponse,
    status_code=status.HTTP_201_CREATED
)

def create_invoice_item(
    invoice_id: int,
    item_data: InvoiceItemCreate,
    db: Session = Depends(get_db)
):

    return invoice_item_service.create_invoice_item(
        db=db,
        invoice_id=invoice_id,
        item_data=item_data
    )


@router.get(
    "",
    response_model=list[InvoiceItemResponse]
)

def get_invoice_items(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    return invoice_item_service.get_invoice_items(
        db=db,
        invoice_id=invoice_id
    )


@router.get(
    "/{item_id}",
    response_model=InvoiceItemResponse
)

def get_invoice_item(
    invoice_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):

    return invoice_item_service.get_invoice_item(
        db=db,
        invoice_id=invoice_id,
        item_id=item_id
    )


@router.patch(
    "/{item_id}",
    response_model=InvoiceItemResponse
)

def update_invoice_item(
    invoice_id: int,
    item_id: int,
    item: InvoiceItemUpdate,
    db: Session = Depends(get_db)
):

    return invoice_item_service.update_invoice_item(
        db=db,
        invoice_id=invoice_id,
        item_id=item_id,
        item=item
    )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_invoice_item(
    invoice_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):

    invoice_item_service.delete_invoice_item(
        db=db,
        invoice_id=invoice_id,
        item_id=item_id
    )
