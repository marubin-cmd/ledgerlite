from sqlalchemy import Column, Date, ForeignKey, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name =  Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    category_type = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    transactions = relationship(
        "Transaction",
        back_populates="category"
    )
