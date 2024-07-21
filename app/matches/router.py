# import datetime
#
# from fastapi import APIRouter, Response, Depends, Request, HTTPException
# from starlette import status
#
# from app.users.auth import create_access_token, get_password_hash, verify_password
# from app.users.dao import UsersDAO
# from app.statistics.dao import StatisticsDAO
# from app.users.dependencies import get_user
#
# from app.users.models import Users
#
# router = APIRouter(
#     prefix="/user",
#     tags=["Auth & User"]
# )
#
#
# @router.get("/showMyStatistic",
#             summary="Get info about auth user",
#             description="This endpoint for get info about auth user"
#             )
# async def info_user(current_user: Users = Depends(get_user)) -> dict:
#     statistics = await StatisticsDAO.find_one_or_none(user_id=current_user.id)
#     return {
#         'id': current_user.id,
#         'user': {
#             'id': current_user.id,
#             'email': current_user.email,
#             'username': current_user.username,
#             'inGame': False,
#             'createdAt': datetime.date(2020, 11, 11),
#             'roles': ['user', ],
#         },
#         'totalGamesPlayed': statistics.games,
#         'wins': statistics.wins,
#         'losses': statistics.losses,
#         'draws': statistics.draws,
#         'rating': statistics.rating,
#     }
