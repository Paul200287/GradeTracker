from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from app.database.session import Base
from sqlalchemy.orm import relationship
from app.models.role import Role

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)