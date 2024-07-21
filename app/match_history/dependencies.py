from datetime import datetime

import jwt
from fastapi import Depends, WebSocket, HTTPException
from starlette import status

from app.config import ALGORITHM, ACCESS_SECRET_KEY

from app.users.dao import UsersDAO


async def socket_get_user(token: str):
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return user
