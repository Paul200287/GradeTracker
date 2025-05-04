from sqlalchemy.orm import Session
from app.models.exam import Exam
from app.models.subject import Subject
from app.schemas.exam import ExamCreate, ExamRead, ExamUpdate
from datetime import datetime

def get_exam(db: Session, exam_id: int):
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    
    if not db_exam:
        return None
    
    return db_exam

def get_exams(db: Session):
    return db.query(Exam).filter(Exam.deleted_at == None).all()

def create_exam(db: Session, exam_data: ExamCreate):
    if not db.query(Subject).filter(Subject.id == exam_data.subject_id).first():
        return None

    db_exam = Exam(
        title=exam_data.title,
        date=exam_data.date,
        type=exam_data.type,
        weight=exam_data.weight,
        max_score=exam_data.max_score,
        subject_id=exam_data.subject_id
    )

    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)

    return db_exam

def update_exam(db: Session, exam_id: int, exam_data: ExamUpdate):
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not db_exam:
        return None
    
    update_data = exam_data.dict(exclude_unset=True)

    for key, val in update_data.items():
        setattr(db_exam, key, val)

    db.commit()
    db.refresh(db_exam)

    return db_exam

def delete_exam(db: Session, exam_id: int):
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not db_exam:
        return None

    db_exam.deleted_at = datetime.utcnow()
    db.commit()

    return True