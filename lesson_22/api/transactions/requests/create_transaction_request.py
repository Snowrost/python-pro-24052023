from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


class CreateTransactionRequest(BaseModel):
    amount: int
    transaction_date: datetime = None
    description: Optional[constr(max_length=100)] = None
