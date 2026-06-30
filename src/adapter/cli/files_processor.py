import logging
from dataclasses import dataclass
from pathlib import Path

from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from entities import Student
from gateways import StudentReportGateway
from services import HomologableSubjectsService, StudentReportService
from subject_repository import SubjectRepository

from .progress_bar import CLIProgressBar


@dataclass(frozen=True)
class CLIFilesProcessor:
    _subject_repository: SubjectRepository
    _report_gateway: StudentReportGateway
    _logger: logging.Logger

    def process_files(self, files: list[Path]):
        for file in files:
            progress = CLIProgressBar(file)

            progress.advance("Processing file")

            self._logger.info(f"processing file {file}")

            student = self._build_student_from(file, progress)

            self._logger.info("    generating report")

            progress.advance("Generating report")

            report_result = StudentReportService(
                self._report_gateway,
                self._logger
            ).generate_report(student)

            self._logger.info(f"    report generated at {report_result}")

            progress.advance("Report generated")

            progress.end()

    def _build_student_from(self, file: Path, progress: CLIProgressBar) -> Student:
        self._logger.info("    parsing pdf text")

        info_gateway = PDFStudentInfoGateway(self._logger, file)

        progress.advance("Obtaining homologable subjects")

        self._logger.info("    obtaining homologable subjects")

        homologable_subjects = HomologableSubjectsService(
            self._subject_repository,
            info_gateway,
            self._logger
        ).suggest_subjects()

        progress.advance("Building student data")

        return Student(
            info_gateway.get_name(),
            info_gateway.get_identification(),
            homologable_subjects
        )
