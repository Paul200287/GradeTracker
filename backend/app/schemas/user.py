from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.role import Role

class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=15)
    email: EmailStr = Field(..., min_length=7, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=50)
    role: Role

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    role: Role 

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
