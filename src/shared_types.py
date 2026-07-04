from typing import TypeAlias, Mapping

Semester: TypeAlias = int
Grade: TypeAlias = float

SubjectCode: TypeAlias = int
SubjectName: TypeAlias = str
SubjectCredits: TypeAlias = int

# one subject can have more than one prerequisite
SubjectPrerequisites: TypeAlias = Mapping[SubjectCode, list[SubjectCode]]

StudentName: TypeAlias = str
StudentIdentification: TypeAlias = int
StudentGrades: TypeAlias = Mapping[SubjectCode, Grade]

ReportGenerationResult: TypeAlias = str
