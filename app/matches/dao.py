from app.matches.models import Matches
from app.dao.base import BaseDAO
from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker


class MatchesDAO(BaseDAO):
    model = Matches

    @classmethod
    async def find_one_or_none_by_user(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                (cls.model.white_id == user_id) | (cls.model.black_id == user_id), cls.model.end == False)
            result = await session.execute(query)
            return result.scalar_one_or_none()
