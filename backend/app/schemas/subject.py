from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubjectBase(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    semester: Optional[str] = None
    teacher_name: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    semester: Optional[str] = None
    teacher_name: Optional[str] = None
