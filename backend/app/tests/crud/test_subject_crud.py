import pytest
from app.models.subject import Subject
from app.models.role import Role
from app.schemas.subject import SubjectCreate, SubjectUpdate
from app.crud import subject as crud
from app.exceptions.subject import *
from app.exceptions.exam import *
from app.exceptions.grade import *


def test_create_subject_as_editor(db, test_editor):
    subject_data = SubjectCreate(
        user_id=test_editor.id,
        name="Math",
        description="Algebra and Geometry",
        semester="1",
        teacher_name="Dr. Euler"
    )
    subject = crud.create_subject(db, subject_data, owner_id=test_editor.id)
    assert subject.name == "Math"
    assert subject.user_id == test_editor.id


def test_create_subject_invalid_owner(db, test_editor):
    subject_data = SubjectCreate(
        user_id=999,  # different user
        name="Physics",
        description="Mechanics",
        semester="2",
        teacher_name="Dr. Newton"
    )
    with pytest.raises(InvalidSubjectOwner):
        crud.create_subject(db, subject_data, owner_id=test_editor.id)


def test_get_subject_as_owner(db, test_editor):
    subject_data = SubjectCreate(
        user_id=test_editor.id,
        name="Chemistry",
        description="Organic Chemistry",
        semester="2",
        teacher_name="Dr. Curie"
    )
    subject = crud.create_subject(db, subject_data, owner_id=test_editor.id)
    fetched = crud.get_subject(db, subject.id, owner_id=test_editor.id)
    assert fetched.id == subject.id


def test_update_subject_as_editor(db, test_editor):
    subject_data = SubjectCreate(
        user_id=test_editor.id,
        name="Biology",
        description="Cells and DNA",
        semester="1",
        teacher_name="Dr. Darwin"
    )
    subject = crud.create_subject(db, subject_data, owner_id=test_editor.id)
    update_data = SubjectUpdate(name="Advanced Biology")
    updated = crud.update_subject(db, subject.id, update_data, owner_id=test_editor.id)
    assert updated.name == "Advanced Biology"


def test_delete_subject(db, test_editor):
    subject_data = SubjectCreate(
        user_id=test_editor.id,
        name="Geography",
        description="Earth Science",
        semester="3",
        teacher_name="Dr. Humboldt"
    )
    subject = crud.create_subject(db, subject_data, owner_id=test_editor.id)
    result = crud.delete_subject(db, subject.id, owner_id=test_editor.id)
    assert result is True
    assert subject.deleted_at is not None


def test_delete_subject_twice_raises(db, test_editor):
    subject_data = SubjectCreate(
        user_id=test_editor.id,
        name="Philosophy",
        description="Ethics and Logic",
        semester="4",
        teacher_name="Plato"
    )
    subject = crud.create_subject(db, subject_data, owner_id=test_editor.id)
    crud.delete_subject(db, subject.id, owner_id=test_editor.id)

    with pytest.raises(SubjectAlreadyDeleted):
        crud.delete_subject(db, subject.id, owner_id=test_editor.id)


def test_get_nonexistent_subject_raises(db, test_editor):
    with pytest.raises(SubjectNotFound):
        crud.get_subject(db, subject_id=9999, owner_id=test_editor.id)
