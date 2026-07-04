import logging

import pytest

from adapter.subject_repository.sqlite import SQLiteSubjectRepository
from services import PendingSubjectsService

DEFAULT_DATABASE_PATH = "transition_plan.db"
PENDING_SUBJECTS_AT_CAREER_START = 27

@pytest.fixture
def pending_subjects_service():
    logger = logging.getLogger()
    subject_repository = SQLiteSubjectRepository(DEFAULT_DATABASE_PATH, logger)

    return PendingSubjectsService(subject_repository, logger)

def test_pending_subjects(pending_subjects_service):
    want = PENDING_SUBJECTS_AT_CAREER_START

    pending_subjects = pending_subjects_service.get_pending_subjects([])
    got = len(pending_subjects)

    assert want == got
