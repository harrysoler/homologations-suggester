from dataclasses import dataclass
from logging import Logger

from student_info_gateway import StudentInfoGateway
from shared_types import StudentGrades, SubjectCode
from subject_repository import SubjectRepository
from entities import ApprovedSubject, OldPensumSubject, NewPensumSubject

@dataclass(frozen=True)
class SuggestSubjectsService:
    _subject_repository: SubjectRepository
    _student_info_gateway: StudentInfoGateway
    _logger: Logger

    def suggest_homologable_subjects(self) -> list[ApprovedSubject]:
        student_grades: StudentGrades = self._student_info_gateway.get_graded_subjects()

        passed_subject_codes = self._filter_approved_subjects(student_grades)

        # find metadata of old passed subjects
        passed_subjects = list(map(self._find_subject_by_code, passed_subject_codes))

        # filter the homologable subjects
        return list(filter(None, map(self._find_homologable_subject, passed_subjects)))

    def _find_homologable_subject(self, old_subject: OldPensumSubject | NewPensumSubject) -> ApprovedSubject:
        if isinstance(old_subject, NewPensumSubject):
            return None

        homologable_subject = self._subject_repository.find_homologable_subject_for(old_subject.code)

        if not homologable_subject:
            return None

        return ApprovedSubject(old_subject, homologable_subject)

    # A previously approved subject can be from the old or new pensum
    def _find_subject_by_code(self, code: SubjectCode) -> OldPensumSubject | NewPensumSubject | None:
        old_pensum_subject = self._subject_repository.find_old_subject_by_code(code)

        if old_pensum_subject:
            return old_pensum_subject

        new_pensum_subject = self._subject_repository.find_new_subject_by_code(code)

        if new_pensum_subject:
            return new_pensum_subject

        self._logger.error("subject %s not found in subjects", code)

        return None
    
    def _filter_approved_subjects(self, subjects: StudentGrades) -> list[SubjectCode]:
        return [
            subject_id for subject_id, grade in subjects.items() if self._is_grade_approved(grade)
        ]

    def _is_grade_approved(self, grade: float) -> bool:
        return grade >= 3.0
