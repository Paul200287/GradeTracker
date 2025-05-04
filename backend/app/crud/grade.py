from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate

def get_grade(db: Session, grade_id: int):
    return db.query(Grade).filter(Grade.id == grade_id).first()

def get_grades(db: Session):
    return db.query(Grade).all()

def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(**grade.dict())

    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)

    return db_grade

def update_grade(db: Session, grade_id: int, grade_update: GradeUpdate):
    db_grade = get_grade(db, grade_id)

    if not db_grade:
        return None
    
    for key, val in grade_update.dict(exclude_unset=True).items():
        setattr(db_grade, key, val)

    db.commit()
    db.refresh(db_grade)

    return db_grade

def delete_grade(db: Session, grade_id: int):
    db_grade = get_grade(db, grade_id)

    if not db_grade:
        return False
    
    db.delete(db_grade)
    db.commit()

    return True
