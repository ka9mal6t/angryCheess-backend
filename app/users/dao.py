from sqlalchemy import select
from sqlalchemy.sql.operators import and_, or_

from app.database import async_session_maker
from app.users.models import Users
from app.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users
