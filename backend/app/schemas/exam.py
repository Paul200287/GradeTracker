from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExamBase(BaseModel):
    title: str
    date: datetime
    type: Optional[str] = None
    weight: Optional[float] = None
    max_score: Optional[float] = None


class ExamCreate(ExamBase):
    subject_id: int


class ExamRead(ExamBase):
    id: int
    subject_id: int
    created_at: datetime
    updated_at: Optional[datetime]
