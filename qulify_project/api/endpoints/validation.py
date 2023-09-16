from fastapi import HTTPException


def is_logged(check_current):
    if check_current is None:
        raise HTTPException(status_code=401, detail="No users currently logged in")


def user_exist(user_exist):
    if user_exist is not None:
        raise HTTPException(status_code=400, detail="Email already registered")


def not_user(user):
    if not user:
        raise HTTPException(status_code=400, detail="User not found")


def wrong_password(user, password):
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid password")

def owner_of_meeting(meetings, user_current):
    if meetings.owner_id != user_current.id:
        raise HTTPException(status_code=403, detail="You do not have permission")


def not_owner_of_meeting(meetings, user_current):
    if meetings.owner_id == user_current.id:
        raise HTTPException(status_code=403, detail="You do not have permission")


def is_participant(participants):
    if participants:
        raise HTTPException(status_code=400, detail="The User is all already a participant in this meeting")


def is_not_participant(participants):
    if not participants:
        raise HTTPException(status_code=400, detail="User is not a participant of this meeting")


def meeting_dont_exists(meeting):
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")


def feedback_dont_exists(feedback):
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")


def feedback_exists(feedback):
    if feedback:
        raise HTTPException(status_code=404, detail="Only 1 comment per Meeting")


def feedback_creator(feedback, user):
    if feedback.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update  or delete this feedback")


def custom_item_exists(custom_item):
    if not custom_item:
        raise HTTPException(status_code=404, detail="Custom item not found")


def check_exists(check):
    if check:
        raise HTTPException(status_code=400, detail="A check for this custom item in this meeting already exists")


def check_dont_exists(check):
    if not check:
        raise HTTPException(status_code=403, detail="A check for this custom item doesnt exists")
