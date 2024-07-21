from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL

engine_async = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
