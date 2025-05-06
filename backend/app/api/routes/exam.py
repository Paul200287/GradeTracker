from fastapi import APIRouter, Depends, status, HTTPException
from app.crud import exam as crud
from app.schemas.exam import ExamBase, ExamCreate, ExamRead, ExamUpdate
from typing import List
from app.api.deps import SessionDep, CurrentUser, get_current_user
from app.models.role import Role
from typing import List
from app.models.subject import Subject
from app.models.user import User
from app.exceptions.exam import *
from app.exceptions.subject import *


router = APIRouter()

# Get a single exam by ID if the user has access
@router.get("/{exam_id}", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_exam(db: SessionDep, exam_id: int, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_exam(db, exam_id, current_user.id)
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

# Get all exams visible to the current user
@router.get("/", response_model=List[ExamRead], dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_exams(db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_exams(db, current_user.id)
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

# Create a new exam (requires editor or superuser)
@router.post("/create-exam", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def create_exam(db: SessionDep, data: ExamCreate, current_user: User=Depends(get_current_user)):
    try:
        return crud.create_exam(db, data, current_user.id)
    except SubjectNotFound:
        raise HTTPException(404, detail="Subject not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

# Update an existing exam (requires editor or superuser)
@router.put("/update-exam/{exam_id}", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def update_exam(db: SessionDep, exam_id: int, new_data: ExamUpdate, current_user: User=Depends(get_current_user)):
    try:
        return crud.update_exam(db, exam_id, new_data, current_user.id)
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")

# Soft-delete an exam (requires editor or superuser)
@router.delete("/delete-exam/{exam_id}", response_model=bool, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def delete_exam(db: SessionDep, exam_id: int, current_user: User=Depends(get_current_user)):
    try:
        return crud.delete_exam(db, exam_id, current_user.id)
    except ExamNotFound:
        raise HTTPException(404, detail="Exam not found.")
    except SubjectAccessDenied:
        raise HTTPException(403, detail="You don't have access to this subject.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")