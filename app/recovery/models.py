from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Recovery(Base):
    __tablename__ = 'recovery'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    code = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="recovery")




