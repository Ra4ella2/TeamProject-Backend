from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    amount_cents = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
