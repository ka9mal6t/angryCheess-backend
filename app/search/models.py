from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Search(Base):
    __tablename__ = 'search'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, primary_key=True)
    rating = Column(Integer, nullable=False)
    time_start = Column(DateTime, nullable=False, default=datetime.now())
