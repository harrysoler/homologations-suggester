from typing import TypeAlias, Mapping

Semester: TypeAlias = int
Grade: TypeAlias = float

SubjectCode: TypeAlias = int
SubjectName: TypeAlias = str
SubjectCredits: TypeAlias = int

StudentIdentification: TypeAlias = int
StudentGrades: TypeAlias = Mapping[SubjectCode, Grade]
