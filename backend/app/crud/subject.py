from app.models.subject import Subject
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectUpdate
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.exceptions.subject import *

def get_subject(db: Session, subject_id: int, owner_id: int):
    """
    Retrieve a subject by ID if the user has access.

    Args:
        db (Session): Database session.
        subject_id (int): ID of the subject to retrieve.
        owner_id (int): ID of the current user.

    Raises:
        SubjectNotFound: If the subject does not exist or access is denied.

    Returns:
        Subject: The subject object.
    """
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
    """
    Retrieve all subjects visible to the current user.

    Args:
        db (Session): Database session.
        owner_id (int): ID of the current user.

    Raises:
        PermissionDenied: If the user is not authenticated.

    Returns:
        List[Subject]: List of subjects accessible to the user.
    """
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can access all subjects
    if current_user.role == Role.SUPERUSER:
        return db.query(Subject).filter(Subject.deleted_at == None).all()

    # Others see only their own subjects
    return db.query(Subject).filter(Subject.deleted_at == None, Subject.user_id == owner_id).all()


def create_subject(db: Session, subject_data: SubjectCreate, owner_id: int):
    """
    Create a new subject if the user is allowed.

    Args:
        db (Session): Database session.
        subject_data (SubjectCreate): Data for the new subject.
        owner_id (int): ID of the current user.

    Raises:
        PermissionDenied: If the user is not an editor or superuser.
        InvalidSubjectOwner: If an editor tries to create a subject for another user.

    Returns:
        Subject: The created subject object.
    """
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
    """
    Update an existing subject if the user has permission.

    Args:
        db (Session): Database session.
        subject_id (int): ID of the subject to update.
        new_data (SubjectUpdate): New data for the subject.
        owner_id (int): ID of the current user.

    Raises:
        SubjectNotFound: If the subject does not exist.
        PermissionDenied: If the user is not allowed to update the subject.

    Returns:
        Subject: The updated subject object.
    """
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
    """
    Soft-delete a subject if the user has permission.

    Args:
        db (Session): Database session.
        subject_id (int): ID of the subject to delete.
        owner_id (int): ID of the current user.

    Raises:
        SubjectNotFound: If the subject does not exist.
        SubjectAlreadyDeleted: If the subject was already deleted.
        PermissionDenied: If the user is not allowed to delete the subject.

    Returns:
        bool: True if the deletion was successful.
    """
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