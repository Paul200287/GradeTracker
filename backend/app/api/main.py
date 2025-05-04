from fastapi import APIRouter

from app.api.routes import login, user, exam, subject, grade

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(exam.router, prefix="/exams", tags=["exams"])
api_router.include_router(subject.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(grade.router, prefix="/grades", tags=["grades"])
