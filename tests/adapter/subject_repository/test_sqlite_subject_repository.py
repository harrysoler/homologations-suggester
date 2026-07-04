import logging

import pytest

from adapter.subject_repository.sqlite import SQLiteSubjectRepository

DEFAULT_DATABASE_PATH = "transition_plan.db"
TOTAL_NEW_PENSUM_SUBJECTS = 48
TOTAL_SUBJECT_PREREQUISITES = 21

@pytest.fixture
def sqlite_subject_repository():
    logger = logging.getLogger()
    return SQLiteSubjectRepository(DEFAULT_DATABASE_PATH, logger)

def test_all_subjects_pending(sqlite_subject_repository):
    want = TOTAL_NEW_PENSUM_SUBJECTS

    pending_subjects = sqlite_subject_repository.find_pending_subjects_from_new_pensum([])    
    got = len(pending_subjects)

    assert want == got

def test_some_subjects_pending(sqlite_subject_repository):
    approved_subjects = [96103, 11701, 31161, 10240, 31160]
    want = TOTAL_NEW_PENSUM_SUBJECTS - len(approved_subjects)

    pending_subjects = sqlite_subject_repository.find_pending_subjects_from_new_pensum(
        approved_subjects
    )
    got = len(pending_subjects)

    assert want == got

def test_subject_prerequisites(sqlite_subject_repository):
    want = TOTAL_SUBJECT_PREREQUISITES

    prerequisites = sqlite_subject_repository.find_all_new_subject_prerequisites()
    got = len(prerequisites)

    assert want == got
