from dataclasses import dataclass

from entities import NewPensumSubject, Student
from shared_types import StudentIdentification, StudentName


@dataclass(frozen=True)
class PendingSubjectsReportData:
    """
    Student pending subjects report details
    """

    name: StudentName
    identification: StudentIdentification
    pending_subjects: list[NewPensumSubject]

    @classmethod
    def from_student(cls, student: Student, pending_subjects: list[NewPensumSubject]):
        return cls(
            name=student.name,
            identification=student.identification,
            pending_subjects=pending_subjects
        )
