from dataclasses import dataclass

from shared_types import StudentName, StudentIdentification
from entities import ApprovedSubject

@dataclass(frozen=True)
class Student:
    """
    All the information of the student grouped into one class
    """

    name: StudentName
    identification: StudentIdentification
    approved_subjects: list[ApprovedSubject]

    def get_total_approved_credits(self) -> int:
        return sum(item.target_subject.credits for item in self.approved_subjects) 
