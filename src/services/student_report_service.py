import logging
from dataclasses import dataclass

from entities import Student
from gateways import StudentReportGateway
from services import HomologableSubjectsService
from shared_types import ReportGenerationResult


@dataclass(frozen=True)
class StudentReportService:
    _report_gateway: StudentReportGateway
    _logger: logging.Logger

    def generate_report(self, student: Student) -> ReportGenerationResult:
        return self._report_gateway.generate_report(student)

    def _build_student(self) -> Student:
        homologable_subjects = HomologableSubjectsService(
            self._subject_repository,
            self._info_gateway,
            self._logger
        ).suggest_subjects()

        return Student(
            self._info_gateway.get_name(),
            self._info_gateway.get_identification(),
            homologable_subjects
        )
        
