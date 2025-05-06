from app.models.subject import Subject
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectUpdate
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.exceptions.subject import *

def get_subject(db: Session, subject_id: int, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can access any subject
    if current_user.role == Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
    else:
        subject = db.query(Subject).filter(Subject.id == subject_id, Subject.user_id == owner_id).first()

    if not subject:
        raise SubjectNotFound()

    return subject


def get_subjects(db: Session, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can access all subjects
    if current_user.role == Role.SUPERUSER:
        return db.query(Subject).filter(Subject.deleted_at == None).all()

    # Others see only their own subjects
    return db.query(Subject).filter(Subject.deleted_at == None, Subject.user_id == owner_id).all()


def create_subject(db: Session, subject_data: SubjectCreate, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    # Editors can only create subjects for themselves
    if current_user.role != Role.SUPERUSER and subject_data.user_id != owner_id:
        raise InvalidSubjectOwner()

    db_subject = Subject(
        user_id=subject_data.user_id,
        name=subject_data.name,
        description=subject_data.description,
        semester=subject_data.semester,
        teacher_name=subject_data.teacher_name
    )

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


def update_subject(db: Session, subject_id: int, new_data: SubjectUpdate, owner_id: int):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    
    if not db_subject:
        raise SubjectNotFound()

    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    if current_user.role != Role.SUPERUSER and db_subject.user_id != owner_id:
        raise PermissionDenied()

    for key, val in new_data.dict(exclude_unset=True).items():
        setattr(db_subject, key, val)

    db.commit()
    db.refresh(db_subject)

    return db_subject


def delete_subject(db: Session, subject_id: int, owner_id: int):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    
    if not db_subject:
        raise SubjectNotFound()

    if db_subject.deleted_at is not None:
        raise SubjectAlreadyDeleted()

    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    # Editors can only delete their own subjects
    if current_user.role != Role.SUPERUSER and db_subject.user_id != owner_id:
        raise PermissionDenied()

    db_subject.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(db_subject)

    return True