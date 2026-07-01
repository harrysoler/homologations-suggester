from typing import NamedTuple

from shared_types import StudentName, StudentIdentification, StudentGrades

class Student(NamedTuple):
    """
    All the information of the student as input
    """

    name: StudentName
    identification: StudentIdentification
    grades: StudentGrades
