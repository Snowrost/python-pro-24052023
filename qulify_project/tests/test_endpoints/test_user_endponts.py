import pytest
from fastapi.testclient import TestClient
from app.service import app
from api.endpoints import get_current_user
from domain.models import User
from tests.sessions import db, clean_data
from sqlalchemy import select

client = TestClient(app)


@pytest.mark.asyncio
async def test_register(db):
    # given
    data = {"email": "test7@example.com", "password": "password"}
    # when
    response = client.post("/users/register", json=data)

    # then
    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful"}

    saved_data = db.execute(select(User).where(User.email =="test7@example.com"))
    saved_data = saved_data.scalar()
    assert saved_data is not None
    assert saved_data.email == "test7@example.com"
    assert saved_data.password == "password"
    clean_data(db, saved_data)


@pytest.mark.asyncio
async def test_register_email_exists(data_processing_instance):
    # given
    data = {"email": "deadbysun45@mail.ma", "password": "password"}
    # when
    response = client.post("/users/register", json=data)

    # then
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_login():
    # given
    data = {"email": "deadbysun45@mail.ma", "password": "498855"}
    # when
    response = client.post("/users/login", json=data)

    # then
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
    user = get_current_user()
    assert user is not None
    assert user.email == "deadbysun45@mail.ma"


@pytest.mark.asyncio
async def test_login_wrong_email():
    # given
    data = {"email": "deadbysun455@mail.ma", "password": "498855"}
    response = client.post("/users/login", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}
    user = get_current_user()
    assert user is None


@pytest.mark.asyncio
async def test_register_wrong_password():
    # given
    data = {"email": "deadbysun45@mail.ma", "password": "4985855"}
    response = client.post("/users/login", json=data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid password"}
    user = get_current_user()
    assert user is None


@pytest.mark.asyncio
async def update_user_data(db):
    # given
    data = {"email": "example562@example.com", "password": "password123"}
    # when
    response = client.post("/users/login", json=data)
    # then
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
    user = get_current_user()
    assert user is not None
    assert user.email == "deadbysun45@mail.ma"
    update_user_data = {
        "name": "Test User",
        "lastname": "UpdatedLastname"}

    response = client.post("/user/update-user", json=update_user_data)
    assert response.status_code == 200
    updated_data = db.execute(select(User).where(User.email == "deadbysun45@mail.ma"))
    updated_data = updated_data.scalar()
    assert updated_data is not None
    assert updated_data.name == "Test User"
    assert updated_data.lastname == "UpdatedLastname"




