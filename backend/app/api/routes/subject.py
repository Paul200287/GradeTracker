from fastapi import APIRouter, Depends, status, HTTPException
from app.crud import subject as crud
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectRead, SubjectUpdate
from typing import List
from app.api.deps import SessionDep, get_current_user
from app.models.user import User
from app.exceptions.subject import *

router = APIRouter()

@router.get("/{subject_id}", response_model=SubjectRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_subject(db: SessionDep, subject_id: int, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_subject(db, subject_id, current_user.id)
    except SubjectNotFound:
        raise HTTPException(404, detail="Subject not found.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")


@router.get("/", response_model=List[SubjectRead], dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def get_subjects(db: SessionDep, current_user: User=Depends(get_current_user)):
    try:
        return crud.get_subjects(db, current_user.id)
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")


@router.post("/create-subject", response_model=SubjectRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def create_subject(db: SessionDep, data: SubjectCreate, current_user: User=Depends(get_current_user)):
    try:
        return crud.create_subject(db, data, current_user.id)
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")
    except InvalidSubjectOwner:
        raise HTTPException(400, detail="Editors can only create subjects for themselves.")


@router.put("/update-subject/{subject_id}", response_model=SubjectRead, dependencies=[Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def update_subject(db: SessionDep, subject_id: int, new_data: SubjectUpdate, current_user: User=Depends(get_current_user)):
    try:
        return crud.update_subject(db, subject_id, new_data, current_user.id)
    except SubjectNotFound:
        raise HTTPException(404, detail="Subject not found.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")


@router.delete("/delete-subject/{subject_id}", response_model=bool, dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
def delete_subject(db: SessionDep, subject_id: int, current_user: User=Depends(get_current_user)):
    try:
        return crud.delete_subject(db, subject_id, current_user.id)
    except SubjectNotFound:
        raise HTTPException(404, detail="Subject not found.")
    except SubjectAlreadyDeleted:
        raise HTTPException(400, detail="Subject already deleted.")
    except PermissionDenied:
        raise HTTPException(403, detail="Permission denied.")
