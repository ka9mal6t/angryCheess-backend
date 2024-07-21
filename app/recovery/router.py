import datetime
from datetime import timedelta

from fastapi import APIRouter, Response, BackgroundTasks, HTTPException
from starlette import status

from app.recovery.dao import RecoveryDAO
from app.recovery.schemas import SRecoveryUser, SNewPass, SCheckCode
from app.recovery.tools import create_unique_reset_code
from app.tasks.tasks import send_reset_pass
from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.models import Users

router = APIRouter(
    prefix="/forgotPassword",
    tags=["Recovery password"]
)


@router.post("/sendRecoverlinkToEmail",
             summary="Recovery password",
             description="This endpoint for recovery password")
async def forgot_password(background_tasks: BackgroundTasks, user_data: SRecoveryUser):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    recovery = await RecoveryDAO.find_one_or_none(user_id=existing_user.id)
    if not recovery or recovery.datetime + timedelta(0, 10 * 60) < datetime.datetime.utcnow():
        await RecoveryDAO.delete(user_id=existing_user.id)
        recovery_code = await create_unique_reset_code()
        await RecoveryDAO.add(user_id=existing_user.id,
                              code=recovery_code,
                              datetime=datetime.datetime.utcnow())

        # ! send code on email
        background_tasks.add_task(send_reset_pass,
                                  email_to=user_data.email,
                                  code=recovery_code)
        return recovery_code
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, )


@router.post("/checkToken")
async def check_code(user_data: SCheckCode):
    recovery = await RecoveryDAO.find_one_or_none(code=user_data.token)
    if not recovery or recovery.datetime + timedelta(0, 10 * 60) < datetime.datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )


@router.post("/changePassword")
async def change_pass(user_data: SNewPass):
    recovery = await RecoveryDAO.find_one_or_none(code=user_data.token)
    if not recovery or recovery.datetime + timedelta(0, 10 * 60) < datetime.datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    user = await UsersDAO.find_one_or_none(id=recovery.user_id)
    await UsersDAO.update({'password': get_password_hash(user.email, user_data.newPassword)}, id=recovery.user_id)
    await RecoveryDAO.delete(user_id=recovery.user_id)
