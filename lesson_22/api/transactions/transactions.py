from fastapi import APIRouter

from domain.transactions import TransactionCreator
from domain.transactions.reports import transactions_report

from .requests import CreateTransactionRequest

transactions_router = APIRouter()


@transactions_router.post("/transactions")
async def create_transaction(request: CreateTransactionRequest):
    transaction_id = await TransactionCreator().create_transaction(
        **request.model_dump()
    )
    return {"id": transaction_id}


@transactions_router.get("/transactions/report")
async def get_transactions_report():
    report = await transactions_report()
    return report
