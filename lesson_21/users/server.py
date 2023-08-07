from uuid import uuid4
import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
async def create_card(user_id):
    await asyncio.sleep(0.1)
    return {
        "id": str(uuid4()),
        "first_name": "John",
        "last_name": "Dough",
        "kyc_status": "PASSED",
    }
