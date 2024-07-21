import datetime

from fastapi import APIRouter, Response, Depends, Request, HTTPException
from starlette import status

from app.statistics.dao import StatisticsDAO
from app.users.auth import create_access_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.users.dependencies import get_user

from app.users.models import Users
from app.users.schemas import SUserRegister, SUserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth & User"]
)


@router.post("/register",
             summary="Register new user",
             description="This endpoint for register new user"
             )
async def register_user(user_data: SUserRegister):
    existing_user1 = await UsersDAO.find_one_or_none(username=user_data.username)
    existing_user2 = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user1 or existing_user2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    user = await UsersDAO.add(email=user_data.email, username=user_data.username,
                              password=get_password_hash(user_data.email,
                                                         user_data.password))
    await StatisticsDAO.add(user_id=user.id, rating=1000)


@router.post("/login",
             summary="Login as user",
             description="This endpoint for auth as user"
             )
async def login_user(user_data: SUserLogin):
    user: Users = await UsersDAO.find_one_or_none(username=user_data.username)
    if not user or not verify_password(user.email + user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return {'accessToken': create_access_token({"sub": str(user.id)})}
