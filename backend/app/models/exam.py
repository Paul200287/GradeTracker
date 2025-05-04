from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.session import Base
import datetime


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    title = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    type = Column(String(50), nullable=True)
    weight = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    subject = relationship("Subject", back_populates="exam")
    grades = relationship("Grade", back_populates="exam")

from app.models.subject import Subject
from app.models.grade import Grade