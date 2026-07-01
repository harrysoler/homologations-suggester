from dataclasses import dataclass

from shared_types import StudentName, StudentIdentification, StudentGrades
from entities import ApprovedSubject

@dataclass(frozen=True)
class StudentAnalysis:
    """
    All the information gathered from the student
    """

    name: StudentName
    identification: StudentIdentification
    grades: StudentGrades
    approved_subjects: list[ApprovedSubject]

    def get_total_approved_credits(self) -> int:
        return sum(item.target_subject.credits for item in self.approved_subjects) 
