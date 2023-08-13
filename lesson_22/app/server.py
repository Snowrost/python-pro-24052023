from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware

from api.transactions import transactions_router
from core.middlewares import SQLAlchemyMiddleware


def init_routers(_app: FastAPI) -> None:
    _app.include_router(transactions_router)


def middlewares() -> List[Middleware]:
    return [Middleware(SQLAlchemyMiddleware)]


def create_app() -> FastAPI:
    _app = FastAPI(middleware=middlewares())
    init_routers(_app=_app)
    return _app


app = create_app()
