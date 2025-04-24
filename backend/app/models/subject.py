from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum
import datetime


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    semester = Column(String(20), nullable=True)
    teacher_name = Column(String(100), nullable=True)
    color = Column(String(7), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    users = relationship("SubjectUser", back_populates="subject", cascade="all, delete-orphan")
