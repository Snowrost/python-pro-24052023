from pydantic import BaseModel
from sqlalchemy import select

from core.db import session
from domain.models import Transaction


class TransactionsReport(BaseModel):
    total: int


async def transactions_report() -> TransactionsReport:
    query = select(Transaction)
    result = await session.execute(query)
    total = 0
    for transaction in result.scalars().all():
        total += transaction.amount

    return TransactionsReport(total=total)
