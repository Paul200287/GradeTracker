from fastapi import APIRouter, Depends, status, HTTPException
from app.crud import exam as crud
from app.schemas.exam import ExamBase, ExamCreate, ExamRead, ExamUpdate
from typing import List
from app.api.deps import SessionDep, CurrentUser, get_current_user
from app.models.role import Role
from typing import List
from app.models.subject import Subject
from app.models.user import User


router = APIRouter()

@router.get("/{exam_id}", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_exam(db: SessionDep, exam_id: int, current_user: User=Depends(get_current_user)):
    db_exam = crud.get_exam(db, exam_id, current_user.id)

    if not db_exam:
        raise HTTPException(404, detail="Exam not found or not enough permissions!")
    
    return db_exam

@router.get("/", response_model=List[ExamRead], dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_exams(db: SessionDep, current_user: User=Depends(get_current_user)):
    db_exams = crud.get_exams(db, current_user.id)

    if not db_exams:
        raise HTTPException(404, detail="Not enough permissions!")
    
    return db_exams

@router.post("/create-exam", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def create_exam(db: SessionDep, data: ExamCreate, current_user: User=Depends(get_current_user)):
    db_exam = crud.create_exam(db, data, current_user.id)

    if not db_exam:
        raise HTTPException(400, detail="Subject not found or not enough permissions!")
    
    return db_exam

@router.put("/update-exam/{exam_id}", response_model=ExamRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def update_exam(db: SessionDep, exam_id: int, new_data: ExamUpdate, current_user: User=Depends(get_current_user)):
    db_exam = crud.update_exam(db, exam_id, new_data, current_user.id)

    if not db_exam:
        raise HTTPException(400, detail="Something went wrong!")
    
    return db_exam

@router.delete("/delete-exam/{exam_id}", response_model=bool, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def delete_exam(db: SessionDep, exam_id: int, current_user: User=Depends(get_current_user)):
    success = crud.delete_exam(db, exam_id, current_user.id)

    if not success:
        raise HTTPException(404, detail="Exam not found!")
    
    return success