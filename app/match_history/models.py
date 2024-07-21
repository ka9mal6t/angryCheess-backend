from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean, PrimaryKeyConstraint, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class MatchHistory(Base):
    __tablename__ = 'match_history'

    match_id = Column(Integer, ForeignKey('matches.id', ondelete='CASCADE'), nullable=False)
    move_number = Column(Integer, nullable=False)
    board = Column(JSON, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'move_number', name='match_pk'),
    )
