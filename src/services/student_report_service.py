import logging
from dataclasses import dataclass

from entities import Student
from gateways import StudentInfoGateway, StudentReportGateway
from services import HomologableSubjectsService
from shared_types import ReportGenerationResult
from subject_repository import SubjectRepository


@dataclass(frozen=True)
class StudentReportService:
    _info_gateway: StudentInfoGateway
    _report_gateway: StudentReportGateway
    _subject_repository: SubjectRepository
    _logger: logging.Logger

    def generate_report(self) -> ReportGenerationResult:
        student = self._build_student()

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
        
