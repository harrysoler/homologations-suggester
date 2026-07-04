from typing import Protocol

from entities import OldPensumSubject, NewPensumSubject
from shared_types import SubjectCode


class SubjectRepository(Protocol):
    def find_old_subject_by_code(subject_code: SubjectCode) -> OldPensumSubject | None:
        ...

    def find_new_subject_by_code(subject_code: SubjectCode) -> NewPensumSubject | None:
        ...

    def find_homologable_subject_for(old_subject_code: SubjectCode) -> NewPensumSubject | None:
        ...

    def find_pending_subjects_from_new_pensum(approved_subjects: list[SubjectCode]) -> list[NewPensumSubject]:
        """
        Get all the subjects from the new pensum excluding the already approved
        """
        ...
