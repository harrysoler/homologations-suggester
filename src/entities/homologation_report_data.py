from dataclasses import dataclass

from shared_types import StudentName, StudentIdentification, StudentGrades
from entities import ApprovedSubject, Student

@dataclass(frozen=True)
class HomologationReportData:
    """
    Student homologation report details
    """

    name: StudentName
    identification: StudentIdentification
    grades: StudentGrades
    approved_subjects: list[ApprovedSubject]

    @classmethod
    def from_student(cls, student: Student, approved_subjects: list[ApprovedSubject]):
        return cls(
            name=student.name,
            identification=student.identification,
            grades=student.grades,
            approved_subjects=approved_subjects
        )

    def get_total_approved_credits(self) -> int:
        return sum(item.target_subject.credits for item in self.approved_subjects) 
