from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.grade_enum import GradeEnum

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    grade = Column(Enum(GradeEnum), nullable=False)

    exam = relationship("Exam", back_populates="grades")