from fastapi import APIRouter, HTTPException, Depends
from core.db.repository import DataProcessing
from domain.models import Meeting, Participant, User
from api.endpoints import (get_current_user, is_logged, meeting_dont_exists, is_participant, owner_of_meeting,
                           is_not_participant, not_owner_of_meeting)

router = APIRouter()
data_processing = DataProcessing()


@router.post("/add-user-to-meeting/{meeting_id}/{user_id}")
async def add_user_to_meeting(meeting_id: str, user_ids: list[str], current_user=Depends(get_current_user)):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    owner_of_meeting(meeting, current_user)
    for user_id in user_ids:
        user = await data_processing.get_data_from_model_filter(User, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        existing_participant = await data_processing.get_data_from_model_filter(
            Participant,
            meeting_id=meeting_id,
            user_id=user_id
        )
        is_participant(existing_participant)
        participant_data = {
            "meeting_id": meeting_id,
            "user_id": user_id,
        }
        await data_processing.save_data(Participant, participant_data)
    return {"message": "User added to the meeting successfully"}


@router.post("/join-meeting/{meeting_id}")
async def join_meeting_as_participant(meeting_id: str, current_user=Depends(get_current_user), ):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    not_owner_of_meeting(meeting, current_user)
    existing_participant = await data_processing.get_data_from_model_filter(
        Participant,
        meeting_id=meeting_id,
        user_id=current_user.id,
    )
    is_participant(existing_participant)
    participant_data = {
        "meeting_id": meeting_id,
        "user_id": current_user.id,
    }
    await data_processing.save_data(Participant, participant_data)
    return {"message": "You have successfully joined the meeting as a participant"}


@router.delete("/leave-meeting/{meeting_id}")
async def leave_meeting_as_participant(
        meeting_id: str,
        current_user=Depends(get_current_user),
):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    not_owner_of_meeting(meeting, current_user)
    participant = await data_processing.get_data_from_model_filter(
        Participant,
        meeting_id=meeting_id,
        user_id=current_user.id,
    )
    is_participant(participant)
    await data_processing.delete_data(Participant, id=participant.id)
    return {"message": "You have successfully left the meeting as a participant"}


@router.delete("/delete-participant/{meeting_id}/{user_id}")
async def delete_participant_from_meeting(
        meeting_id: str,
        user_ids: list[str],
        current_user=Depends(get_current_user),
):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    owner_of_meeting(meeting, current_user)
    for user_id in user_ids:
        participant = await data_processing.get_data_from_model_filter(
            Participant,
            meeting_id=meeting_id,
            user_id=user_id,
        )
        is_not_participant(participant)
        await data_processing.delete_data(Participant, id=participant.id)
    return {"message": "Participants deleted successfully"}


