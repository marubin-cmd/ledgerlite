from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    transaction_date = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    category_id = Column(
    Integer,
    ForeignKey("categories.id"),
    nullable=True,
    )

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=True,
        unique=True
    )

    category = relationship(
        "Category",
        back_populates="transactions"
    )

    payment = relationship(
    "Payment",
    back_populates="transaction"
    )