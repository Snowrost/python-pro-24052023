from fastapi import APIRouter, Depends
from core.db.repository import DataProcessing
from domain.models import CustomItem
from api.endpoints import get_current_user, is_logged


router = APIRouter()
data_processing = DataProcessing()


@router.post("/create-custom-item/")
async def create_custom_item(item_name: str, price: float, current_user=Depends(get_current_user)):
    is_logged(current_user)
    custom_item_data = {
        "item_name": item_name,
        "price": price,
    }
    await data_processing.save_data(CustomItem, custom_item_data)

    return {"message": "Custom item created successfully"}
