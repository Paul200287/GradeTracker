from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate
from app.exceptions.grade import *
from app.exceptions.subject import *
from app.exceptions.exam import *
from app.models.user import User
from app.models.role import Role
from app.models.subject import Subject
from app.models.exam import Exam

def get_grade(db: Session, grade_id: int, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    # Get the grade
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise GradeNotFound()

    # Superuser has full access
    if current_user.role == Role.SUPERUSER:
        return grade

    # Get the exam
    exam = db.query(Exam).filter(Exam.id == grade.exam_id).first()
    if not exam:
        raise ExamNotFound()

    # Get the subject
    subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()
    if not subject or subject.user_id != owner_id:
        raise SubjectAccessDenied()

    return grade


def get_grades(db: Session, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    if current_user.role == Role.SUPERUSER:
        return db.query(Grade).all()

    return db.query(Grade).join(Exam).join(Subject).filter(Subject.user_id == owner_id).all()


def create_grade(db: Session, grade_data: GradeCreate, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    # Get the related exam
    exam = db.query(Exam).filter(Exam.id == grade_data.exam_id).first()
    if not exam:
        raise ExamNotFound()

    # Get the subject from the exam
    subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()
    if not subject:
        raise SubjectNotFound()

    if current_user.role != Role.SUPERUSER and subject.user_id != owner_id:
        raise SubjectAccessDenied()

    try:
        db_grade = Grade(**grade_data.dict())
    except Exception:
        raise InvalidGradeData()

    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)

    return db_grade


def update_grade(db: Session, grade_id: int, grade_update: GradeUpdate, owner_id: int):
    db_grade = get_grade(db, grade_id, owner_id)

    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    # Get the exam and subject
    exam = db.query(Exam).filter(Exam.id == db_grade.exam_id).first()
    if not exam:
        raise ExamNotFound()

    subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()
    if not subject or subject.user_id != owner_id:
        raise SubjectAccessDenied()

    for key, val in grade_update.dict(exclude_unset=True).items():
        setattr(db_grade, key, val)

    db.commit()
    db.refresh(db_grade)

    return db_grade


def delete_grade(db: Session, grade_id: int, owner_id: int):
    db_grade = get_grade(db, grade_id, owner_id)

    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user or current_user.role not in [Role.SUPERUSER, Role.EDITOR]:
        raise PermissionDenied()

    exam = db.query(Exam).filter(Exam.id == db_grade.exam_id).first()
    if not exam:
        raise ExamNotFound()

    subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()
    if not subject or subject.user_id != owner_id:
        raise SubjectAccessDenied()

    db.delete(db_grade)
    db.commit()

    return True