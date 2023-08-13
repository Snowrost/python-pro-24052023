from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Integer, Unicode

from core.db import Base
from core.db.mixins import TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(UUID, primary_key=True, default=uuid4())
    amount = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.now())
    description = Column(Unicode(100), nullable=True)
