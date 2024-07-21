from app.search.models import Search
from app.dao.base import BaseDAO
from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker


class SearchDAO(BaseDAO):
    model = Search

    @classmethod
    async def find_one_or_none_filter(cls, rating):
        async with async_session_maker() as session:
            query = select(cls.model) .filter(
                (cls.model.rating >= rating - 250) & (cls.model.rating <= rating + 250)).order_by(
                cls.model.time_start)
            result = await session.execute(query)
            return result.scalar_one_or_none()

