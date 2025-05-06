from sqlalchemy.orm import Session
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.user import User
from app.models.role import Role
from app.schemas.exam import ExamCreate, ExamRead, ExamUpdate
from datetime import datetime
from app.exceptions.exam import *
from app.exceptions.subject import *


def get_exam(db: Session, exam_id: int, owner_id: int):
    """
    Retrieve a single exam by ID if the user has access.

    Args:
        db (Session): Database session.
        exam_id (int): ID of the exam to retrieve.
        owner_id (int): ID of the current user.

    Raises:
        ExamNotFound: If the exam does not exist or access is denied.

    Returns:
        Exam: The exam object.
    """
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can access any exam
    if current_user.role == Role.SUPERUSER:
        db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    else:
        db_exam = db.query(Exam).join(Subject).filter(Exam.id == exam_id, Subject.user_id == owner_id).first()

    if not db_exam:
        raise ExamNotFound()

    return db_exam


def get_exams(db: Session, owner_id: int):
    """
    Retrieve all exams visible to the current user.

    Args:
        db (Session): Database session.
        owner_id (int): ID of the current user.

    Returns:
        List[Exam]: List of exam objects accessible to the user.
    """
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can access all exams
    if current_user.role == Role.SUPERUSER:
        return db.query(Exam).filter(Exam.deleted_at == None).all()

    # Others only their own
    return db.query(Exam).join(Subject).filter(Exam.deleted_at == None, Subject.user_id == owner_id).all()


def create_exam(db: Session, exam_data: ExamCreate, owner_id: int):
    """
    Create a new exam if the user is allowed.

    Args:
        db (Session): Database session.
        exam_data (ExamCreate): Data for the new exam.
        owner_id (int): ID of the current user.

    Raises:
        SubjectNotFound: If the subject does not exist.
        SubjectAccessDenied: If the user does not own the subject.
        PermissionDenied: If the user is not an editor or superuser.

    Returns:
        Exam: The created exam object.
    """
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Superuser can create exam for any subject
    if current_user.role == Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == exam_data.subject_id).first()
        if not subject:
            raise SubjectNotFound()
    else:
        # Editor must own the subject
        subject = db.query(Subject).filter(Subject.id == exam_data.subject_id, Subject.user_id == owner_id).first()

        if not subject:
            raise SubjectAccessDenied()
        if current_user.role != Role.EDITOR:
            raise PermissionDenied()

    new_exam = Exam(
        title=exam_data.title,
        date=exam_data.date,
        type=exam_data.type,
        weight=exam_data.weight,
        max_score=exam_data.max_score,
        subject_id=exam_data.subject_id
    )

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return new_exam


def update_exam(db: Session, exam_id: int, exam_data: ExamUpdate, owner_id: int):
    """
    Update an existing exam if the user has permission.

    Args:
        db (Session): Database session.
        exam_id (int): ID of the exam to update.
        exam_data (ExamUpdate): New data for the exam.
        owner_id (int): ID of the current user.

    Raises:
        ExamNotFound: If the exam does not exist.
        SubjectAccessDenied: If the user does not own the subject.
        PermissionDenied: If the user is not an editor or superuser.

    Returns:
        Exam: The updated exam object.
    """
    # Get the exam to update
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not db_exam:
        raise ExamNotFound()

    current_user = db.query(User).filter(User.id == owner_id).first()

    # Check permissions
    if current_user.role != Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == db_exam.subject_id).first()
        if not subject or subject.user_id != owner_id:
            raise SubjectAccessDenied()
        if current_user.role != Role.EDITOR:
            raise PermissionDenied()

    update_data = exam_data.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(db_exam, key, val)

    db.commit()
    db.refresh(db_exam)

    return db_exam


def delete_exam(db: Session, exam_id: int, owner_id: int):
    """
    Soft-delete an exam if the user has permission.

    Args:
        db (Session): Database session.
        exam_id (int): ID of the exam to delete.
        owner_id (int): ID of the current user.

    Raises:
        ExamNotFound: If the exam does not exist.
        SubjectAccessDenied: If the user does not own the subject.
        PermissionDenied: If the user is not an editor or superuser.

    Returns:
        bool: True if deletion was successful.
    """
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not db_exam:
        raise ExamNotFound()

    current_user = db.query(User).filter(User.id == owner_id).first()

    # Check permissions
    if current_user.role != Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == db_exam.subject_id).first()
        if not subject or subject.user_id != owner_id:
            raise SubjectAccessDenied()
        if current_user.role != Role.EDITOR:
            raise PermissionDenied()

    db_exam.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exam)

    return True