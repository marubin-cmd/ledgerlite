from datetime import date, datetime
from typing import Literal
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    AliasPath
)


class InvoiceCreate(BaseModel):

    client_id: int = Field(gt=0)

    type: Literal["income", "expense"]

    issue_date: date
    due_date: date

    notes: str | None = None

    @model_validator(mode="after")

    def validate_dates(self):
        if self.due_date < self.issue_date:
            raise ValueError("Due date cannot be earlier than issue date")

        return self


class InvoiceUpdate(BaseModel):

    client_id: int | None = Field(default=None, gt=0)

    type: Literal["income", "expense"] | None = None

    issue_date: date | None = None
    due_date: date | None = None

    notes: str | None = None


class InvoiceResponse(BaseModel):

    id: int
    client_id: int
    invoice_number: str

    type: Literal["income", "expense"]

    issue_date: date
    due_date: date

    status: Literal[
    "draft",
    "unpaid",
    "partially_paid",
    "paid",
    "overdue",
    "cancelled"
    ]

    notes: str | None

    created_at: datetime
    updated_at: datetime

    subtotal: Decimal
    total: Decimal

    amount_paid: Decimal
    balance: Decimal

    model_config=ConfigDict(from_attributes=True)


class DashboardInvoiceResponse(BaseModel):

    id: int
    client_id: int

    client_name: str = Field(
        validation_alias=AliasPath("client", "name")
    )

    invoice_number: str

    type: Literal["income", "expense"]

    issue_date: date
    due_date: date

    status: Literal[
    "draft",
    "unpaid",
    "partially_paid",
    "paid",
    "overdue",
    "cancelled"
    ]

    notes: str | None

    created_at: datetime
    updated_at: datetime

    subtotal: Decimal
    total: Decimal

    amount_paid: Decimal
    balance: Decimal

    model_config=ConfigDict(from_attributes=True)


