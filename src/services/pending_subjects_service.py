from logging import Logger

from dataclasses import dataclass

from entities import NewPensumSubject
from shared_types import SubjectCode
from subject_repository import SubjectRepository


@dataclass(frozen=True)
class PendingSubjectsService:
    _subject_repository: SubjectRepository
    _logger: Logger

    def get_pending_subjects(self, approved_subjects: list[SubjectCode]) -> list[NewPensumSubject]:
        pending_subjects = self._subject_repository.find_pending_subjects_from_new_pensum(approved_subjects)

        # sort by semester and prioritize main subjects
        pending_subjects = sorted(
            pending_subjects,
            key=lambda subject: (subject.semester, not subject.is_main)
        )

        all_prerequisites = self._subject_repository.find_all_new_subject_prerequisites()

        # filter the subjects without prerequisites achieved
        pending_subjects = list(filter(
            lambda subject: self._is_subject_valid(
                all_prerequisites.get(subject.code),
                approved_subjects
            ),
            pending_subjects
        ))

        return pending_subjects

    def _is_subject_valid(self, prerequisites: list[SubjectCode], approved_subjects: list[SubjectCode]) -> bool:
        if not prerequisites:
            return True

        # are the prerequisites fulfilled?
        return all(map(
            lambda prerequisite: prerequisite in approved_subjects,
            prerequisites
        ))
