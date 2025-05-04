from sqlalchemy.orm import Session
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.user import User
from app.models.role import Role
from app.schemas.exam import ExamCreate, ExamRead, ExamUpdate
from datetime import datetime


def get_exam(db: Session, exam_id: int, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    if current_user and current_user.role == Role.SUPERUSER:
        db_exam = db.query(Exam).filter(Exam.id == exam_id).first()

    else:
        db_exam = db.query(Exam).join(Subject).filter(
            Exam.id == exam_id,
            Subject.user_id == owner_id
        ).first()

    if not db_exam:
        return None
    
    return db_exam

def get_exams(db: Session, owner_id: int):
    current_user = db.query(User).filter(User.id == owner_id).first()

    if current_user and current_user.role == Role.SUPERUSER:
        db_exams = db.query(Exam).filter(Exam.deleted_at == None).all()

    else:
        db_exams = db.query(Exam).join(Subject).filter(
            Exam.deleted_at == None,
            Subject.user_id == owner_id
        ).all()

    if not db_exams:
        return None
    
    return db_exams

def create_exam(db: Session, exam_data: ExamCreate, owner_id: int):    
    current_user = db.query(User).filter(User.id == owner_id).first()

    if current_user and current_user.role == Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == exam_data.subject_id).first()
        if not subject:
            return None
    else:
        subject = db.query(Subject).filter(
            Subject.id == exam_data.subject_id,
            Subject.user_id == owner_id
        ).first()

        if not subject or current_user.role != Role.EDITOR:
            return None

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
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not db_exam:
        return None

    current_user = db.query(User).filter(User.id == owner_id).first()

    if not current_user:
        return None

    if current_user.role != Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == db_exam.subject_id).first()
        if not subject or subject.user_id != owner_id or current_user.role != Role.EDITOR:
            return None

    update_data = exam_data.dict(exclude_unset=True)

    for key, val in update_data.items():
        setattr(db_exam, key, val)

    db.commit()
    db.refresh(db_exam)

    return db_exam


def delete_exam(db: Session, exam_id: int, owner_id: int):
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not db_exam:
        return None

    current_user = db.query(User).filter(User.id == owner_id).first()
    if not current_user:
        return None

    if current_user.role != Role.SUPERUSER:
        subject = db.query(Subject).filter(Subject.id == db_exam.subject_id).first()
        if not subject or subject.user_id != owner_id or current_user.role != Role.EDITOR:
            return None

    db_exam.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exam)

    return True
