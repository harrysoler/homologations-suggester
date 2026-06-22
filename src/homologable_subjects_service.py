from dataclasses import dataclass
from logging import Logger

import utils
from student_info_gateway import StudentInfoGateway
from shared_types import StudentGrades, SubjectCode, Grade
from subject_repository import SubjectRepository
from entities import ApprovedSubject, OldPensumSubject, NewPensumSubject

@dataclass(frozen=True)
class HomologableSubjectsService:
    _subject_repository: SubjectRepository
    _student_info_gateway: StudentInfoGateway
    _logger: Logger

    def suggest_subjects(self) -> list[ApprovedSubject]:
        student_grades: StudentGrades = self._student_info_gateway.get_graded_subjects()

        passed_subject_grades = self._filter_approved_subjects(student_grades)

        # find metadata of old passed subjects
        passed_subjects = list(map(self._find_homologable_subject, passed_subject_grades.items()))

        # filter the homologable subjects
        passed_subjects = list(filter(None, passed_subjects))

        # homologated subjects cant repeat
        return utils.remove_duplicates_for_attribute('target_subject.code', passed_subjects, 'grade')

    def _find_homologable_subject(self, subject_data: tuple[SubjectCode, Grade]) -> ApprovedSubject:
        code, grade = subject_data

        old_subject = self._find_subject_by_code(code)

        if isinstance(old_subject, NewPensumSubject):
            return None

        homologable_subject = self._subject_repository.find_homologable_subject_for(old_subject.code)

        if not homologable_subject:
            return None

        return ApprovedSubject(old_subject, grade, homologable_subject)

    # A previously approved subject can be from the old or new pensum
    def _find_subject_by_code(self, code: SubjectCode) -> OldPensumSubject | NewPensumSubject | None:
        old_pensum_subject = self._subject_repository.find_old_subject_by_code(code)

        if old_pensum_subject:
            return old_pensum_subject

        self._logger.error("subject %s not found in subjects", code)

        raise ValueError(f"subject {code} not found in old pensum list")
    
    def _filter_approved_subjects(self, subjects: StudentGrades) -> StudentGrades:
        return {code: grade for code, grade in subjects.items() if self._is_grade_approved(grade)}

    def _is_grade_approved(self, grade: float) -> bool:
        return grade >= 3.0
