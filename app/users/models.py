from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Sequence
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    inGame = Column(Boolean, nullable=False, default=False)

    recovery = relationship("Recovery", back_populates="user")
    statistic = relationship("Statistics", back_populates="user")



