from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    username: str
    password: str





