import logging
from dataclasses import dataclass

from entities import Student, StudentAnalysis
from gateways import StudentReportGateway
from services import HomologableSubjectsService
from shared_types import ReportGenerationResult


@dataclass(frozen=True)
class StudentReportService:
    _report_gateway: StudentReportGateway
    _homologable_subjects_service: HomologableSubjectsService
    _logger: logging.Logger

    def generate_report_from(self, student: Student) -> ReportGenerationResult:
        analysis = self._build_analysis(student)

        return self._report_gateway.generate_report(analysis)

    def _build_analysis(self, student: Student) -> StudentAnalysis:
        homologable_subjects = (
            self
            ._homologable_subjects_service
            .suggest_subjects(student.grades)
        )

        return StudentAnalysis(
            student.name,
            student.identification,
            student.grades,
            homologable_subjects
        )
        
