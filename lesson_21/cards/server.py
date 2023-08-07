from uuid import uuid4

import httpx
import requests
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json

app = Sanic("cards_app", ctx={"DB_HOST": "127.0.0.1"})


@app.post("/cards")
async def create_card(request: Request) -> HTTPResponse:
    user_id = request.json["user_id"]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8081/users/{user_id}")
    if response.json()["kyc_status"] == "PASSED":
        return json({"id": str(uuid4())})
    else:
        return json(
            {
                "errors": [
                    {"message": "User is not allowed to have a card", "code": "1000"}
                ]
            }
        )


@app.post("/cards-sync")
def create_card_sync(request: Request) -> HTTPResponse:
    user_id = request.json["user_id"]
    response = requests.get(f"http://127.0.0.1:8081/users/{user_id}")
    if response.json()["kyc_status"] == "PASSED":
        return json({"id": str(uuid4())})
    else:
        return json(
            {
                "errors": [
                    {"message": "User is not allowed to have a card", "code": "1000"}
                ]
            }
        )
