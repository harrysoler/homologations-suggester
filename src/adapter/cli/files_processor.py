import logging
from dataclasses import dataclass
from pathlib import Path

from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from entities import Student
from gateways import StudentReportGateway
from services import HomologableSubjectsService, StudentReportService
from subject_repository import SubjectRepository

from .reports_status import CLIReportsStatus


@dataclass(frozen=True)
class CLIFilesProcessor:
    _subject_repository: SubjectRepository
    _report_gateway: StudentReportGateway
    _logger: logging.Logger

    def process_files(self, files: list[Path]):
        status = CLIReportsStatus(len(files))

        for file in files:

            self._logger.info(f"processing file {file}")

            student = self._build_student_from(file)

            self._logger.info("    generating report")

            report_result = StudentReportService(
                self._report_gateway,
                self._logger
            ).generate_report(student)

            self._logger.info(f"    report generated at {report_result}")

            status.add_finished_report(student.name, report_result)

        status.stop()

    def _build_student_from(self, file: Path) -> Student:
        self._logger.info("    parsing pdf text")

        info_gateway = PDFStudentInfoGateway(self._logger, file)

        self._logger.info("    obtaining homologable subjects")

        homologable_subjects = HomologableSubjectsService(
            self._subject_repository,
            info_gateway,
            self._logger
        ).suggest_subjects()

        return Student(
            info_gateway.get_name(),
            info_gateway.get_identification(),
            homologable_subjects
        )
