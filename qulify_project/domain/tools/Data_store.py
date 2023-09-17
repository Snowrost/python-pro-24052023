from pydantic import BaseModel

class UserData:
    def __init__(self, id, name, email, lastname):
        self.id = id
        self.name = name
        self.email = email
        self.lastname = lastname


class Data:
    def __init__(self, id, custom_item_number: float):
        self.id = id
        self.custom_item_number = custom_item_number


class RegisterData(BaseModel):
    email: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str

