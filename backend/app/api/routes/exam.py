from fastapi import APIRouter, Depends, status, HTTPException
from app.crud import exam as crud
from app.schemas.exam import ExamBase, ExamCreate, ExamRead, ExamUpdate
from typing import List
from app.api.deps import SessionDep, CurrentUser, require_role
from app.models.role import Role
from typing import List


router = APIRouter()

@router.get("/{exam_id}", response_model=ExamRead, status_code=status.HTTP_200_OK)
def get_exam(db: SessionDep, exam_id: int):
    db_exam = crud.get_exam(db, exam_id)

    if not db_exam:
        raise HTTPException(404, detail="Exam not found!")
    
    return db_exam

@router.get("/", response_model=List[ExamRead], status_code=status.HTTP_200_OK)
def get_exams(db: SessionDep):
    return crud.get_exams(db)

@router.post("/create-exam", response_model=ExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(db: SessionDep, data: ExamCreate):
    db_exam = crud.create_exam(db, data)

    if not db_exam:
        raise HTTPException(400, detail="Subject not found!")
    
    return db_exam

@router.put("/update-exam/{exam_id}", response_model=ExamRead, status_code=status.HTTP_201_CREATED)
def update_exam(db: SessionDep, exam_id: int, new_data: ExamUpdate):
    db_exam = crud.update_exam(db, exam_id, new_data)

    if not db_exam:
        raise HTTPException(400, detail="Something went wrong!")
    
    return db_exam

@router.delete("/delete-exam/{exam_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_exam(db: SessionDep, exam_id: int):
    success = crud.delete_exam(db, exam_id)

    if not success:
        raise HTTPException(404, detail="Exam not found!")
    
    return success