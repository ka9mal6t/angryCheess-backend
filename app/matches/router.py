import datetime

from fastapi import APIRouter, Response, Depends, Request, HTTPException
from starlette import status

from app.users.auth import create_access_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.matches.dao import MatchessDAO
from app.match_history.dao import MatchHistoryDAO
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
    

@router.get("/gameDetails/{match_id}")
async def gameDetails(current_user: Users = Depends(get_user), match_id: int):
    match = await MatchesDAO.find_one_or_none(id=match_id, end=True)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    match_history = await MatchHistoryDAO.find_all(match_id=match_id)
    return match_history
    

@router.get("/gameOnlineDetails/{match_id}")
async def gameOnlineDetails(current_user: Users = Depends(get_user), match_id: int):
    match = await MatchesDAO.find_one_or_none(id=match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    match_history = await MatchHistoryDAO.find_all(match_id=match_id)
    return match_history
        
    
    
