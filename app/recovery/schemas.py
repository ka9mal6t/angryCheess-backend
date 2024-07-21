from typing import Optional

from pydantic import BaseModel, EmailStr


class SRecoveryUser(BaseModel):
    email: EmailStr


class SNewPass(BaseModel):
    newPassword: str
    token: str


class SCheckCode(BaseModel):
    token: str
