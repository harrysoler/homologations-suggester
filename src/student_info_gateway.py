from typing import Protocol

from shared_types import StudentIdentification, StudentGrades, StudentName

class StudentInfoGateway(Protocol):
    """
    Acts as a source of student information to work with
    """
    def get_name(self) -> StudentName:
        ...

    def get_identification(self) -> StudentIdentification:
        ...

    def get_graded_subjects(self) -> StudentGrades:
        ...

    

