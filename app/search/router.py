from fastapi import APIRouter, Depends, Request, HTTPException
from starlette import status

from app.matches.dao import MatchesDAO
from app.matches.models import Matches
from app.search.models import Search
from app.statistics.dao import StatisticsDAO
from app.users.auth import create_access_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.search.dao import SearchDAO
from app.users.dependencies import get_user
import random

from app.users.models import Users

router = APIRouter(
    prefix="/requests",
    tags=["Search Requests"]
)


@router.post("/search",
             summary="Get info about auth user",
             description="This endpoint for get info about auth user"
             )
async def search(current_user: Users = Depends(get_user)):
    statistics = await StatisticsDAO.find_one_or_none(user_id=current_user.id)
    search_match: Search = await SearchDAO.find_one_or_none_filter(rating=statistics.rating)
    myself = await SearchDAO.find_one_or_none(user_id=current_user.id)
    if myself is not None or current_user.inGame:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, )
    if search_match is None:
        await SearchDAO.add(user_id=current_user.id, rating=statistics.rating)
        return 'Successfully'
    else:
        await SearchDAO.delete(user_id=search_match.user_id)
        choose = random.choice([True, False])
        if choose:
            await MatchesDAO.add(white_id=current_user.id, black_id=search_match.user_id)
        else:
            await MatchesDAO.add(black_id=current_user.id, white_id=search_match.user_id)
        await UsersDAO.update({'inGame': True}, id=search_match.user_id)
        await UsersDAO.update({'inGame': True}, id=current_user.id)
        return 'Successfully'


@router.post("/stopSearching",
             summary="Get info about auth user",
             description="This endpoint for get info about auth user"
             )
async def stop_searching(current_user: Users = Depends(get_user)):
    myself = await SearchDAO.find_one_or_none(user_id=current_user.id)
    if myself is None or current_user.inGame:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, )
    else:
        await SearchDAO.delete(user_id=current_user.id)
        return 'Successfully'


@router.get("/checkStatusGame",
            summary="Get info about auth user",
            description="This endpoint for get info about auth user"
            )
async def check_status_game(current_user: Users = Depends(get_user)) -> dict:
    if current_user.inGame is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        match: Matches = await MatchesDAO.find_one_or_none_by_user(current_user.id)
        if match:
            return {'match': match.id,
                    'user_id': current_user.id,
                    'color': 0 if match.white_id == current_user.id else 1}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
