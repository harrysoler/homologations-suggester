from typing import Protocol

from entities import Student
from shared_types import ReportGenerationResult

class StudentReportGateway(Protocol):
    """
    Defines the API for generation of reports  
    """

    def generate_report(self, student: Student) -> ReportGenerationResult:
        ...
