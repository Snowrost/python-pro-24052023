from sqlalchemy import select

from domain.models import Transaction
from tests.api import test_client


def test_create_transaction(db):
    # given
    request = {"amount": 100}

    # when
    response = test_client.post("/transactions", json=request)

    # then
    transaction_id = response.json()["id"]
    query = select(Transaction).where(Transaction.id == transaction_id)
    saved_transaction = db.scalar(query)
    assert saved_transaction.amount == 100
