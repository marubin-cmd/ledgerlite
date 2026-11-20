
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PaymentMethod = Literal["cash", "bank_transfer", "other"]

class PaymentCreate(BaseModel):

    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    payment_date: date
    payment_method: PaymentMethod

    reference_number: str | None = Field(default=None, max_length=100)

    notes: str | None = None


class PaymentUpdate(BaseModel):

    amount: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)

    payment_date: date | None = None

    payment_method: PaymentMethod | None = None

    reference_number: str | None = Field(default=None, max_length=100)

    notes: str | None = None


class PaymentResponse(BaseModel):

    id: int
    invoice_id: int
    amount: Decimal
    payment_date: date
    payment_method: PaymentMethod
    reference_number: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)





