from fastapi import APIRouter, HTTPException, Depends
from core.db.repository import DataProcessing
from domain.models import Meeting, Participant, User, Check
from datetime import datetime
from api.endpoints import get_current_user, is_logged, owner_of_meeting, meeting_dont_exists

router = APIRouter()
data_processing = DataProcessing()


@router.post("/create-meeting")
async def create_meeting(meeting_name: str, date_of_activity: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    date_of_activity = datetime.strptime(date_of_activity, "%Y-%m-%d %H:%M")
    meeting_data_dict = {
        "meeting_name": meeting_name,
        "date_of_activity": date_of_activity,
        "owner_id": current_user.id
    }
    await data_processing.save_data(Meeting, meeting_data_dict)
    new_meeting = await data_processing.get_data_from_model_filter(Meeting, **meeting_data_dict)
    await data_processing.save_data(Participant, {"meeting_id": new_meeting.id, "user_id": current_user.id})
    return {"message": "Meeting create successful", " new_meeting_id =": new_meeting.id}


@router.get("/get_meeting_list")
async def get_meeting_list(current_user=Depends(get_current_user)):
    is_logged(current_user)

    meetings = await data_processing.get_data_from_model_all(Meeting)
    meetings_with_participants = []
    for meeting in meetings:
        is_owner = meeting.owner_id == current_user.id
        participants = await data_processing.get_data_all_from_model_filter(Participant, meeting_id=meeting.id)
        participant_names = []
        for participant in participants:
            # Retrieve the participant's name using User.name
            user = await data_processing.get_data_from_model_filter(User, id=participant.user_id)
            participant_name = user.name if user else ""
            participant_names.append(participant_name)

        meetings_with_participants.append({
            "meeting_name": meeting.meeting_name,
            "participants": participant_names,
            "created by current user": is_owner,
        })
    return {"Meetings with Participants": meetings_with_participants}


@router.delete("/delete-meeting/{meeting_id}")
async def delete_meeting_(meeting_id: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    owner_of_meeting(meeting, current_user)
    participants = await data_processing.get_data_all_from_model_filter(Participant, meeting_id=meeting_id)
    for participant in participants:
        check_exists = await data_processing.get_data_from_model_filter(Check, participant_id=participant.id)
        if check_exists:
            raise HTTPException(status_code=400,
                                detail="Cannot delete the meeting as participants have associated custom items in Check")
    await data_processing.delete_data(Participant, meeting_id=meeting_id)
    await data_processing.delete_data(Meeting, id=meeting_id)
    return {"message": "Meeting deleted successfully"}


@router.put("/update-meeting/{meeting_id}")
async def update_meeting(meeting_id: str, meeting_name: str = None, date_of_activity: str = None, current_user=Depends(get_current_user), ):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    owner_of_meeting(meeting, current_user)
    update_dict = {}
    if meeting_name:
        update_dict["meeting_name"] = meeting_name
    if date_of_activity:
        update_dict["date_of_activity"] = datetime.strptime(date_of_activity, "%Y-%m-%d %H:%M")
    await data_processing.update_data(Meeting, update_dict, id=meeting_id)
    return {"message": "Meeting updated successfully"}


@router.get("/get_meeting_by_id/{meeting_id}")
async def get_meeting_by_id(meeting_id: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    is_owner = meeting.owner_id == current_user.id
    participants = await data_processing.get_data_all_from_model_filter(Participant, meeting_id=meeting_id)
    participant_names = []
    for participant in participants:
        user = await data_processing.get_data_from_model_filter(User, id=participant.user_id)
        participant_name = user.name if user else ""
        participant_names.append(participant_name)

    meeting_with_participants = {
        "meeting_name": meeting.meeting_name,
        "participants": participant_names,
        "is_owner": is_owner,
    }
    return {"Meeting with Participants": meeting_with_participants}
