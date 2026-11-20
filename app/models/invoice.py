from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from decimal import Decimal
from app.db.session import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False
    )

    invoice_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    type = Column(String(10), nullable=False)

    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="draft",
        server_default="draft"
    )

    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @property
    def subtotal(self) -> Decimal:
        return sum(
            (item.total for item in self.items),
            Decimal("0.00")
        )

    @property
    def total(self) -> Decimal:
        return self.subtotal


    @property
    def amount_paid(self) -> Decimal:
        return sum((payment.amount for payment in self.payments),
            Decimal("0.00"))


    @property
    def balance(self) -> Decimal:
        return self.total - self.amount_paid


    client = relationship(
        "Client",
        back_populates="invoices"
    )

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="invoice"
    )

