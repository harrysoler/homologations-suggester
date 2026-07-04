import logging
from dataclasses import dataclass

from entities import Student, HomologationReportData
from gateways import HomologationReportGateway
from services import HomologableSubjectsService
from shared_types import ReportGenerationResult


@dataclass(frozen=True)
class StudentReportService:
    _report_gateway: HomologationReportGateway
    _homologable_subjects_service: HomologableSubjectsService
    _logger: logging.Logger

    def generate_report_from(self, student: Student) -> ReportGenerationResult:
        analysis = self._build_report_data(student)

        return self._report_gateway.generate_report(analysis)

    def _build_report_data(self, student: Student) -> HomologationReportData:
        homologable_subjects = (
            self
            ._homologable_subjects_service
            .suggest_subjects(student.grades)
        )

        return HomologationReportData(
            student.name,
            student.identification,
            student.grades,
            homologable_subjects
        )
        
