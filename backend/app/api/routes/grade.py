from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.grade import GradeCreate, GradeUpdate, GradeRead
from app.api.deps import SessionDep, get_current_user
from app.crud import grade as crud
from typing import List
from app.models.user import User
from app.exceptions.exam import *
from app.exceptions.subject import *
from app.exceptions.grade import *

router = APIRouter()

@router.get("/{grade_id}", response_model=GradeRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_grade(grade_id: int, db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_grade(db, grade_id, current_user.id)
    except GradeNotFound:
        raise HTTPException(404, detail="Grade not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this grade.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

@router.get("/", response_model=List[GradeRead], dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_grades(db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_grades(db, current_user.id)
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

@router.post("/create-grade", response_model=GradeRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.create_grade(db, data, current_user.id)
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except SubjectNotFound:
        raise HTTPException(404, detail="Subject not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")
    except InvalidGradeData:
        raise HTTPException(400, detail="Invalid grade data.")

@router.put("/update-grade/{grade_id}", response_model=GradeRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def update_grade(grade_id: int, new_data: GradeUpdate, db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.update_grade(db, grade_id, new_data, current_user.id)
    except GradeNotFound:
        raise HTTPException(404, detail="Grade not found.")
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

@router.delete("/delete-grade/{grade_id}", response_model=bool, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def delete_grade(grade_id: int, db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.delete_grade(db, grade_id, current_user.id)
    except GradeNotFound:
        raise HTTPException(404, detail="Grade not found.")
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")
