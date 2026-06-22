from typing import Protocol, TypeAlias

from entities import Student

GenerationResult: TypeAlias = str

class StudentReportGateway(Protocol):
    """
    Defines the API for generation of reports  
    """

    def generate_report(self, student: Student) -> GenerationResult:
        ...
