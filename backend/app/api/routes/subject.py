from fastapi import APIRouter, Depends, status, HTTPException
from app.crud import subject as crud
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectRead, SubjectUpdate
from typing import List
from app.api.deps import SessionDep

router = APIRouter()

@router.get("/{subject_id}", response_model=SubjectRead, status_code=status.HTTP_200_OK)
def get_subject(db: SessionDep, subject_id: int):
    db_subject = crud.get_subject(db, subject_id)

    if not db_subject:
        raise HTTPException(404, detail="Subject not found!")
    
    return db_subject


@router.get("/", response_model=List[SubjectRead], status_code=status.HTTP_200_OK)
def get_subjects(db: SessionDep):
    return crud.get_subjects(db)


@router.post("/create-subject", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
def create_subject(db: SessionDep, data: SubjectCreate):
    db_subject = crud.create_subject(db, data)

    if not db_subject:
        raise HTTPException(400, detail="Failed to create subject!")
    
    return db_subject


@router.put("/update-subject/{subject_id}", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
def update_subject(db: SessionDep, subject_id: int, new_data: SubjectUpdate):
    db_subject = crud.update_subject(db, subject_id, new_data)

    if not db_subject:
        raise HTTPException(400, detail="Something went wrong while updating!")
    
    return db_subject


@router.delete("/delete-subject/{subject_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_subject(db: SessionDep, subject_id: int):
    success = crud.delete_subject(db, subject_id)

    if not success:
        raise HTTPException(404, detail="Subject not found!")
    
    return success
