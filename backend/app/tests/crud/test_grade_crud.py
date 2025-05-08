import pytest
from app.crud import grade as crud
from app.schemas.grade import GradeCreate, GradeUpdate
from app.models.grade_enum import GradeEnum
from app.crud import subject as subject_crud
from app.crud import exam as exam_crud
from app.schemas.subject import SubjectCreate
from app.schemas.exam import ExamCreate
from app.exceptions.subject import *
from app.exceptions.exam import *
from app.exceptions.grade import *

def create_subject_and_exam(db, user):
    subject_data = SubjectCreate(
        user_id=user.id,
        name="Testfach",
        description="Beschreibung",
        semester="1",
        teacher_name="Prof. Beispiel"
    )
    subject = subject_crud.create_subject(db, subject_data, user.id)

    exam_data = ExamCreate(
        title="Schularbeit",
        date="2025-01-01",
        type="schriftlich",
        weight=1.0,
        max_score=100,
        subject_id=subject.id
    )
    exam = exam_crud.create_exam(db, exam_data, user.id)
    return exam


def test_create_grade_success(db, test_editor):
    exam = create_subject_and_exam(db, test_editor)

    grade_data = GradeCreate(
        exam_id=exam.id,
        grade=GradeEnum.gut
    )

    grade = crud.create_grade(db, grade_data, owner_id=test_editor.id)
    assert grade.exam_id == exam.id
    assert grade.grade == GradeEnum.gut


def test_create_grade_exam_not_found(db, test_editor):
    grade_data = GradeCreate(
        exam_id=9999,
        grade=GradeEnum.sehr_gut
    )

    with pytest.raises(ExamNotFound):
        crud.create_grade(db, grade_data, owner_id=test_editor.id)


def test_create_grade_subject_access_denied(db, test_superuser, test_editor):
    exam = create_subject_and_exam(db, test_superuser)

    grade_data = GradeCreate(
        exam_id=exam.id,
        grade=GradeEnum.befriedigend
    )

    with pytest.raises(SubjectAccessDenied):
        crud.create_grade(db, grade_data, owner_id=test_editor.id)


def test_update_grade_success(db, test_editor):
    exam = create_subject_and_exam(db, test_editor)

    grade = crud.create_grade(
        db, GradeCreate(exam_id=exam.id, grade=GradeEnum.genuegend), test_editor.id
    )

    updated = crud.update_grade(
        db, grade_id=grade.id,
        grade_update=GradeUpdate(grade=GradeEnum.sehr_gut),
        owner_id=test_editor.id
    )
    assert updated.grade == GradeEnum.sehr_gut


def test_update_grade_not_found(db, test_editor):
    with pytest.raises(GradeNotFound):
        crud.update_grade(
            db,
            grade_id=9999,
            grade_update=GradeUpdate(grade=GradeEnum.gut),
            owner_id=test_editor.id
        )


def test_update_grade_no_permission(db, test_superuser, test_editor):
    exam = create_subject_and_exam(db, test_superuser)
    grade = crud.create_grade(
        db, GradeCreate(exam_id=exam.id, grade=GradeEnum.befriedigend), test_superuser.id
    )

    with pytest.raises(SubjectAccessDenied):
        crud.update_grade(
            db,
            grade_id=grade.id,
            grade_update=GradeUpdate(grade=GradeEnum.nicht_genuegend),
            owner_id=test_editor.id
        )


def test_delete_grade_success(db, test_editor):
    exam = create_subject_and_exam(db, test_editor)
    grade = crud.create_grade(
        db, GradeCreate(exam_id=exam.id, grade=GradeEnum.genuegend), test_editor.id
    )

    result = crud.delete_grade(db, grade_id=grade.id, owner_id=test_editor.id)
    assert result is True


def test_delete_grade_not_found(db, test_editor):
    with pytest.raises(GradeNotFound):
        crud.delete_grade(db, grade_id=9999, owner_id=test_editor.id)


def test_delete_grade_subject_access_denied(db, test_superuser, test_editor):
    exam = create_subject_and_exam(db, test_superuser)
    grade = crud.create_grade(
        db, GradeCreate(exam_id=exam.id, grade=GradeEnum.gut), test_superuser.id
    )

    with pytest.raises(SubjectAccessDenied):
        crud.delete_grade(db, grade_id=grade.id, owner_id=test_editor.id)