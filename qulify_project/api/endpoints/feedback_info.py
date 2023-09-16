from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from core.db.repository import DataProcessing
from domain.models import Meeting, Feedback, User, Participant
from api.endpoints import (get_current_user, is_logged, meeting_dont_exists, feedback_dont_exists, feedback_creator,
                           is_not_participant, feedback_exists)
from core.db import session, set_session_context, reset_session_context

router = APIRouter()
data_processing = DataProcessing()


@router.post("/create-feedback/{meeting_id}")
async def create_feedback_for_meeting(meeting_id: str, feedback_text: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    if meeting.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="You are the owner of this meeting and cannot create feedback")
    participant = await data_processing.get_data_from_model_filter(Participant, meeting_id=meeting_id, user_id=current_user.id)
    is_not_participant(participant)
    feedback_data = {
        "user_id": current_user.id,
        "meeting_id": meeting_id,
        "comment": feedback_text
    }
    await data_processing.save_data(Feedback, feedback_data)
    return {"message": "Feedback created successfully"}


@router.put("/update-feedback/{feedback_id}")
async def update_feedback(feedback_id: str,updated_text: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    feedback = await data_processing.get_data_from_model_filter(Feedback, id=feedback_id)
    feedback_dont_exists(feedback)
    feedback_creator(feedback, current_user)
    feedback.comment = updated_text
    await data_processing.update_data(Feedback, {"comment": updated_text}, id=feedback_id)
    return {"message": "Feedback updated successfully"}


@router.delete("/delete-feedback/{feedback_id}")
async def delete_feedback(feedback_id: str, current_user=Depends(get_current_user)):
    is_logged(current_user)
    feedback = await data_processing.get_data_from_model_filter(Feedback, id=feedback_id)
    feedback_dont_exists(feedback)
    feedback_creator(feedback, current_user)
    await data_processing.delete_data(Feedback, id=feedback_id)

    return {"message": "Feedback deleted successfully"}


@router.get("/feedbacks-for-meeting/{meeting_id}")
async def get_feedbacks_for_meeting(meeting_id: str, current_user=Depends(get_current_user)):
    is_logged(current_user)

    meeting = await data_processing.get_data_from_model_filter(Meeting, id=meeting_id)
    meeting_dont_exists(meeting)
    query = (
        select(Feedback.comment, User.name, Feedback.created_at)
        .join(User)
        .where(Feedback.meeting_id == meeting_id)
    )
    token = set_session_context("query")
    async with session() as db:
        result = await db.execute(query)
        reset_session_context(token)
    rows = result.fetchall()
    feedback_data = [{"comment": row[0], "created_by": row[1], "created_at": row[2]}for row in rows]

    return feedback_data


@router.get("/get_user-feedbacks")
async def get_user_feedbacks(current_user=Depends(get_current_user)):
    is_logged(current_user)
    query = (
        select(Feedback.comment, Meeting.meeting_name, Feedback.created_at)
        .join(Meeting)
        .where(Feedback.user_id == current_user.id)
    )

    token = set_session_context("query")
    async with (session() as db):
        result = await db.execute(query)
        reset_session_context(token)

    rows = result.fetchall()

    feedback_data = [{"comment": row[0], "created_for meeting": row[1], "created_at": row[2]} for row in rows]

    return {"user_feedback": feedback_data}



