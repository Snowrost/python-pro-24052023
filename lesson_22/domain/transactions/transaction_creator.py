from datetime import datetime

from core.db import session
from domain.models import Transaction


class TransactionCreator:
    async def create_transaction(
            self, amount: int, transaction_date: datetime, description: str
    ):
        transaction = Transaction(
            amount=amount, transaction_date=transaction_date, description=description
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction.id
