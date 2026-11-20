from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    CheckConstraint,
    func
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Payment(Base):

    __tablename__ = "payments"

    __table_args__ = (

        CheckConstraint(
            "payment_method IN ('cash', 'bank_transfer', 'others')",
            name="check_payment_method"
        ),

        CheckConstraint(
            "amount > 0",
            name="check_payment_amount"
        )

    )

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    amount = Column(Numeric(10,2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(30), nullable=False)
    reference_number = Column(String(100), nullable=True)
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

    invoice = relationship("Invoice", back_populates="payments")

    transaction = relationship("Transaction", back_populates="payment", uselist=False, cascade="all, delete-orphan")