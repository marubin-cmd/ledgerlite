from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)


class InvoiceItemUpdate(BaseModel):

    description: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=255
    )

    quantity: int | None = Field(
        default=None,
        gt=0,
    )


    unit_price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2
    )


class InvoiceItemResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    invoice_id: int
    description: str
    quantity: int
    unit_price: Decimal
    total: Decimal
