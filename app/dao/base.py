from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, **params):
        async with async_session_maker() as session:
            query = delete(cls.model).where(*[getattr(cls.model, key) == value for key, value in params.items()]
                                            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, values, **params):
        async with async_session_maker() as session:
            query = update(cls.model).where(*[getattr(cls.model, key) == value for key, value in params.items()])
            query = query.values(values)
            await session.execute(query)
            await session.commit()
