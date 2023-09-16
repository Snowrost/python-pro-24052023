from fastapi import APIRouter, HTTPException, Depends
from core.db.repository import DataProcessing, split_bill_calculate
from domain.models import Meeting, Participant, User, CustomItem, Check
from domain.tools import Data
from api.endpoints import (get_current_user, is_logged, meeting_dont_exists,
                           custom_item_exists, check_exists, check_dont_exists, is_not_participant)
from core.db import session, reset_session_context, set_session_context
from sqlalchemy import select
from typing import List

router = APIRouter()
data_processing = DataProcessing()

# Create a check for a custom item in a meeting
@router.post("/create-check/{meeting_id}/{custom_item_id}/{participant_id}")
async def create_check_with_participants(
    meeting_id: str,
    custom_item_id: str,
    custom_item_number: float,
    participant_ids: List[str] = None,  # Accept a list of participant IDs in the request body
    current_user=Depends(get_current_user),
):
    is_logged(current_user)
    custom_item = await data_processing.get_data_from_model_filter(CustomItem, id=custom_item_id)
    custom_item_exists(custom_item)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    existing_participant = await data_processing.get_data_from_model_filter(Participant, meeting_id=meeting_id,
                                                                            user_id=current_user.id)
    is_not_participant(existing_participant)


   #TODO add create check from here


    existing_check = await data_processing.get_data_from_model_filter(Check, custom_item_id=custom_item_id)
    check_exists(existing_check)
    if participant_ids is not None:
        split = split_bill_calculate(participant_ids, custom_item, custom_item_number)
        for participant_id in participant_ids:
            # Check if the participant exists and is part of the specified meeting
            participant = await data_processing.get_data_from_model_filter(Participant, id=participant_id, meeting_id=meeting_id)
            if not participant:
                raise HTTPException(status_code=404, detail=f"Participant {participant_id} not found in this meeting")
            check_data = {
                "participant_id": participant_id,
                "custom_item_id": custom_item_id,
                "custom_item_number": custom_item_number,
                "splited_bill": split,
            }
            await data_processing.save_data(Check, check_data)
    else:
        participants = await data_processing.get_data_all_from_model_filter(Participant, meeting_id=meeting_id)
        split_for_all = split_bill_calculate(participants, custom_item, custom_item_number)
        for participant in participants:
            check_data = {
                "participant_id": participant.id,
                "custom_item_id": custom_item_id,
                "custom_item_number": custom_item_number,
                "splited_bill": split_for_all
            }
            await data_processing.save_data(Check, check_data)
    return {"message": "Check created successfully"}


@router.delete("/delete-custom-item/{meeting_id}/{custom_item_id}")
async def delete_custom_item(meeting_id: str, custom_item_id: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    custom_item = await data_processing.get_data_from_model_filter(CustomItem, id=custom_item_id)
    custom_item_exists(custom_item)
    existing_participant = await data_processing.get_data_from_model_filter(Participant, meeting_id=meeting_id,
                                                                            user_id=current_user.id)
    is_not_participant(existing_participant)
    await data_processing.delete_data(Check, custom_item_id=custom_item_id)
    await data_processing.delete_data(CustomItem, id=custom_item_id)
    return {"message": "Custom item and associated check records deleted successfully"}

#TODO number update

@router.put("/update-check/{meeting_id}/{custom_item_id}")
async def update_check(
    meeting_id: str,
    custom_item_id: str,
    name: str = None,
    price: float = None,
    current_user=Depends(get_current_user),
):
    is_logged(current_user)
    custom_item = await data_processing.get_data_from_model_filter(CustomItem, id=custom_item_id)
    custom_item_exists(custom_item)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    existing_participant = await data_processing.get_data_from_model_filter(Participant, meeting_id=meeting_id,
                                                                            user_id=current_user.id)
    is_not_participant(existing_participant)
    if name is not None:
        await data_processing.update_data(CustomItem, {"item_name": name}, id=custom_item_id)
    if price is not None:
        await data_processing.update_data(CustomItem, {"price": price}, id=custom_item_id)
        bills = await data_processing.get_data_all_from_model_filter(Check, custom_item_id=custom_item_id)
        updated_item = await data_processing.get_data_from_model_filter(CustomItem, id=custom_item_id)
        token = set_session_context("some_context")
        try:
            async with session() as db:
                get_number = await db.execute(
                    select(Check)
                    .where(Check.custom_item_id == custom_item_id))
                get_number = get_number.scalar()
                number = Data(id=get_number.id, custom_item_number=get_number.custom_item_number)
        finally:
            reset_session_context(token)
        update_split = {
            "splited_bill": split_bill_calculate(bills, updated_item, number.custom_item_number)
        }
        await data_processing.update_data(Check, update_split, custom_item_id=custom_item_id)
    return {"message": "Check and custom item updated successfully"}

@router.delete("/delete_particpant_from_check/{meeting_id}/{custom_item_id}")
async def update_check(
    meeting_id: str,
    custom_item_id: str,
    participant_ids: list[str],
    current_user=Depends(get_current_user),
):
    is_logged(current_user)
    # Check if the custom item exists
    custom_item = await data_processing.get_data_from_model_filter(CustomItem, id=custom_item_id)
    custom_item_exists(custom_item)
    # Check if the meeting exists
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    # Check if the user is a participant of the meeting (participants can work with checks)
    existing_participant = await data_processing.get_data_from_model_filter(Participant, meeting_id=meeting_id,
                                                                            user_id=current_user.id)
    is_not_participant(existing_participant)
    existing_check = await data_processing.get_data_from_model_filter(Check, custom_item_id=custom_item_id)
    check_dont_exists(existing_check)
    for participant_id in participant_ids:
        # Check if the participant exists and is part of the specified meeting
        participant = await data_processing.get_data_from_model_filter(Participant, id=participant_id,
                                                                       meeting_id=meeting_id)
        if not participant:
            raise HTTPException(status_code=404, detail=f"Participant {participant_id} not found in this meeting")
        await data_processing.delete_data(Check, participant_id=participant.id)
    bills = await data_processing.get_data_all_from_model_filter(Check, custom_item_id=custom_item_id)
    token = set_session_context("some_context")
    try:
        async with session() as db:
            get_number = await db.execute(
                select(Check)
                .where(Check.custom_item_id == custom_item_id))
            get_number = get_number.scalar()
            number = Data(id=get_number.id, custom_item_number=get_number.custom_item_number)
    finally:
        reset_session_context(token)
    update_split = {
        "splited_bill": split_bill_calculate(bills, custom_item, number.custom_item_number)
    }
    await data_processing.update_data(Check, update_split, custom_item_id=custom_item_id)
    return {"message": "Removed from check participants successfully"}


@router.get("/user_check/{meeting_id}")
async def user_check(
        meeting_id: str,
        current_user=Depends(get_current_user),
):
    is_logged(current_user)
    # Check if the meeting exists
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    # Check if the user is a participant in the meeting
    participant = await data_processing.get_data_from_model_filter(Participant, user_id=current_user.id, meeting_id=meeting_id)
    is_not_participant(participant)
    query = (select(CustomItem.item_name, Check.splited_bill, Check.custom_item_number)
             .join(Check)
             .where(Check.participant_id == participant.id)
    )
    token = set_session_context("query")
    async with session() as db:
        results = await db.execute(query)
        reset_session_context(token)
    rows = results.fetchall()
    user_check = sum(row[1] for row in rows)
    check_data = [{"item_name": row[0], "price": row[1], "number of position": row[2]} for row in rows]
    return {"Check": check_data, "total amount": user_check}


@router.get("/meeting_check/{meeting_id}")
async def meeting_check(
    meeting_id: str,
    current_user=Depends(get_current_user),
):
    is_logged(current_user)
    # Check if the meeting exists
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    participants = await data_processing.get_data_all_from_model_filter(Participant, meeting_id=meeting_id)
    participant_totals={}
    check_data=[]
    for participant in participants:
        query = (
            select(CustomItem.item_name, Check.splited_bill, Check.custom_item_number)
            .join(Check)
            .where(Check.participant_id == participant.id)
        )
        token = set_session_context("query")
        async with session() as db:
            results = await db.execute(query)
            reset_session_context(token)
        rows = results.fetchall()
        check_explain = [{"item_name": row[0], "price": row[1], "number of position": row[2]} for row in rows]
        total_splited_bill = sum(row[1] for row in rows)  # Calculate the sum of splited_bill for the participant
        # participant_totals[participant.user_id] = {"check_data": check_data, "total_splited_bill": total_splited_bill}
        user = await data_processing.get_data_from_model_filter(User, id=participant.user_id)
        participant_name = user.name if user else ""
        check_data.append({
            "participant_name": participant_name,  # Add participant's name to the response
            "check_name": check_explain,  # Get the check_name from the first row
            "total_splited_bill": total_splited_bill,
        })
    return {"Check Data": check_data}



