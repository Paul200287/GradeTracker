import pytest
from datetime import datetime
from app.crud import exam as crud
from app.crud import subject as subject_crud
from app.schemas.exam import ExamCreate, ExamUpdate
from app.schemas.subject import SubjectCreate
from app.exceptions.subject import *
from app.exceptions.exam import *
from app.exceptions.grade import *

def create_subject(db, user):
    subject_data = SubjectCreate(
        user_id=user.id,
        name="Testfach",
        description="Beschreibung",
        semester="1",
        teacher_name="Prof. Beispiel"
    )
    return subject_crud.create_subject(db, subject_data, user.id)


def test_create_exam_success(db, test_editor):
    subject = create_subject(db, test_editor)

    exam_data = ExamCreate(
        title="Mathe Schularbeit",
        date=datetime(2025, 1, 15),
        type="schriftlich",
        weight=0.3,
        max_score=100,
        subject_id=subject.id
    )

    exam = crud.create_exam(db, exam_data, owner_id=test_editor.id)
    assert exam.title == "Mathe Schularbeit"
    assert exam.subject_id == subject.id


def test_create_exam_subject_not_found(db, test_editor):
    exam_data = ExamCreate(
        title="Fehlendes Fach",
        date=datetime(2025, 1, 20),
        type="mündlich",
        weight=0.2,
        max_score=50,
        subject_id=9999
    )

    with pytest.raises(SubjectAccessDenied):
        crud.create_exam(db, exam_data, owner_id=test_editor.id)


def test_create_exam_subject_access_denied(db, test_superuser, test_editor):
    subject = create_subject(db, test_superuser)

    exam_data = ExamCreate(
        title="Nicht erlaubt",
        date=datetime(2025, 1, 25),
        type="schriftlich",
        weight=0.5,
        max_score=80,
        subject_id=subject.id
    )

    with pytest.raises(SubjectAccessDenied):
        crud.create_exam(db, exam_data, owner_id=test_editor.id)


def test_get_exam_success(db, test_editor):
    subject = create_subject(db, test_editor)
    exam = crud.create_exam(
        db,
        ExamCreate(
            title="Schularbeit",
            date=datetime(2025, 2, 1),
            type="schriftlich",
            weight=0.4,
            max_score=90,
            subject_id=subject.id
        ),
        owner_id=test_editor.id
    )

    fetched = crud.get_exam(db, exam.id, owner_id=test_editor.id)
    assert fetched.id == exam.id
    assert fetched.title == exam.title


def test_get_exam_not_found(db, test_editor):
    with pytest.raises(ExamNotFound):
        crud.get_exam(db, exam_id=9999, owner_id=test_editor.id)


def test_update_exam_success(db, test_editor):
    subject = create_subject(db, test_editor)
    exam = crud.create_exam(
        db,
        ExamCreate(
            title="Alt",
            date=datetime(2025, 2, 10),
            type="mündlich",
            weight=0.2,
            max_score=40,
            subject_id=subject.id
        ),
        owner_id=test_editor.id
    )

    update_data = ExamUpdate(title="Neu")
    updated = crud.update_exam(db, exam.id, update_data, owner_id=test_editor.id)
    assert updated.title == "Neu"


def test_update_exam_no_access(db, test_superuser, test_editor):
    subject = create_subject(db, test_superuser)
    exam = crud.create_exam(
        db,
        ExamCreate(
            title="Geschützt",
            date=datetime(2025, 3, 1),
            type="schriftlich",
            weight=0.5,
            max_score=100,
            subject_id=subject.id
        ),
        owner_id=test_superuser.id
    )

    with pytest.raises(SubjectAccessDenied):
        crud.update_exam(db, exam.id, ExamUpdate(title="Verboten"), owner_id=test_editor.id)


def test_delete_exam_success(db, test_editor):
    subject = create_subject(db, test_editor)
    exam = crud.create_exam(
        db,
        ExamCreate(
            title="Zum Löschen",
            date=datetime(2025, 3, 15),
            type="schriftlich",
            weight=1.0,
            max_score=100,
            subject_id=subject.id
        ),
        owner_id=test_editor.id
    )

    result = crud.delete_exam(db, exam.id, owner_id=test_editor.id)
    assert result is True
    assert exam.deleted_at is not None


def test_delete_exam_not_found(db, test_editor):
    with pytest.raises(ExamNotFound):
        crud.delete_exam(db, exam_id=9876, owner_id=test_editor.id)


def test_delete_exam_no_access(db, test_superuser, test_editor):
    subject = create_subject(db, test_superuser)
    exam = crud.create_exam(
        db,
        ExamCreate(
            title="Geschützt löschen",
            date=datetime(2025, 3, 25),
            type="schriftlich",
            weight=1.0,
            max_score=100,
            subject_id=subject.id
        ),
        owner_id=test_superuser.id
    )

    with pytest.raises(SubjectAccessDenied):
        crud.delete_exam(db, exam.id, owner_id=test_editor.id)
