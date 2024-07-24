import datetime

from fastapi import APIRouter, Response, Depends, Request, HTTPException
from starlette import status

from app.users.auth import create_access_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.statistics.dao import StatisticsDAO
from app.users.dependencies import get_user

from app.users.models import Users

router = APIRouter(
    prefix="/matchInfo",
    tags=["Auth & User"]
)


@router.get("/gameResults/{match_id}")
async def game_result(current_user: Users = Depends(get_user), match_id: int):
    match = await MatchesDAO.find_one_or_none(id=match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    return match
    
