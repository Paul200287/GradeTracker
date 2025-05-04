from app.models.subject import Subject
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectUpdate
from datetime import datetime
from sqlalchemy.orm import Session

def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()


def get_subjects(db: Session):
    return db.query(Subject).filter(Subject.deleted_at == None).all()


def create_subject(db: Session, subject_data: SubjectCreate):
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


def update_subject(db: Session, subject_id: int, new_data: SubjectUpdate):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not db_subject:
        return None

    for key, val in new_data.dict(exclude_unset=True).items():
        setattr(db_subject, key, val)

    db.commit()
    db.refresh(db_subject)

    return db_subject


def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not db_subject:
        return None
    
    if db_subject.deleted_at != None:
        return None

    db_subject.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(db_subject)

    return True
