from fastapi import APIRouter, HTTPException
from core.db.repository import DataProcessing
from domain.models import User
from domain.tools import UserData, LoginData, RegisterData
from api.endpoints import is_logged, user_exist, not_user, wrong_password

router = APIRouter()
data_processing = DataProcessing()
current_user = None


# Register endpoint
@router.post("/register")
async def register_user(data: RegisterData):
    email = data.email
    password = data.password
    existing_user = await data_processing.get_data_from_model_filter(User, email=email)
    user_exist(existing_user)
    await data_processing.save_data(User, {"email": email, "password": password})
    return {"message": "Registration successful"}


# Login endpoint
@router.post("/login")
async def login_user(data: LoginData):
    global current_user
    email = data.email
    password = data.password
    user = await data_processing.get_data_from_model_filter(User, email=email)
    not_user(user)
    wrong_password(user,password)
    current_user = UserData(id=user.id, name=user.name, email=user.email, lastname=user.lastname, )
    return {"message": "Login successful"}


# Update user data endpoint
@router.put("/update-user")
async def update_user_data(name: str = None,lastname: str = None, password: str = None, email: str = None,):
    is_logged(get_current_user())
    update_dict = {}
    if name:
        update_dict["name"] = name
    if lastname:
        update_dict["lastname"] = lastname
    if password:
        update_dict["password"] = password
    if email:
        existing_email_user = await data_processing.get_data_from_model_filter(User, email=email)
        if existing_email_user and existing_email_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email is already in use by another user")
        update_dict["email"] = email
    await data_processing.update_data(User, update_dict, id=current_user.id)
    return {"message": "User data updated successfully"}


@router.post("/logout")
async def logout_user():
    global current_user
    current_user = None
    return {"message": "Logout successful"}


def get_current_user():
    return current_user
