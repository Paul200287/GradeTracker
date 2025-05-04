from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.grade import GradeCreate, GradeUpdate, GradeRead
from app.api.deps import SessionDep
from app.crud import grade as crud
from typing import List

router = APIRouter()

@router.get("/{grade_id}", response_model=GradeRead, status_code=status.HTTP_200_OK)
def get_grade(grade_id: int, db: SessionDep):
    grade = crud.get_grade(db, grade_id)

    if not grade:
        raise HTTPException(404, detail="Grade not found!")
    
    return grade

@router.get("/", response_model=List[GradeRead], status_code=status.HTTP_200_OK)
def get_grades(db: SessionDep):
    return crud.get_grades(db)

@router.post("/create-grade", response_model=GradeRead, status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, db: SessionDep):
    return crud.create_grade(db, data)

@router.put("/update-grade/{grade_id}", response_model=GradeRead, status_code=status.HTTP_200_OK)
def update_grade(grade_id: int, new_data: GradeUpdate, db: SessionDep):
    grade = crud.update_grade(db, grade_id, new_data)

    if not grade:
        raise HTTPException(400, detail="Grade update failed!")
    
    return grade

@router.delete("/delete-grade/{grade_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_grade(grade_id: int, db: SessionDep):
    success = crud.delete_grade(db, grade_id)

    if not success:
        raise HTTPException(404, detail="Grade not found!")
    
    return success
