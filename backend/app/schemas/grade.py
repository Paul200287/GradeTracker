from pydantic import BaseModel
from app.models.grade_enum import GradeEnum

class GradeBase(BaseModel):
    grade: GradeEnum

class GradeCreate(GradeBase):
    exam_id: int

class GradeUpdate(GradeBase):
    pass

class GradeRead(GradeBase):
    exam_id: int
