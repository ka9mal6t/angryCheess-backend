from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Matches(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    winner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, default=None)
    end = Column(Boolean, nullable=False, default=False)
    white_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    black_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_start = Column(DateTime, nullable=False, default=datetime.now())
    time_end = Column(DateTime, nullable=True, default=None)
