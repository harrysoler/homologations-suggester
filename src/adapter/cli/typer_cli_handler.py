from logging import Logger
from pathlib import Path
from typing import Annotated, TypeAlias

import rich
import typer

import utils
from constants import (
    DEFAULT_HOMOLOGATION_REPORTS_DIR,
    DEFAULT_PENDING_SUBJECTS_REPORTS_DIR,
)
from entities import ApprovedSubject, HomologationReportData, PendingSubjectsReportData
from gateways import (
    HomologationReportGateway,
    PendingSubjectsReportGateway,
    StudentInfoGateway,
)
from services import (
    HomologableSubjectsService,
    PendingSubjectsService,
    StudentReportService,
)
from shared_types import SubjectCode
from subject_repository import SubjectRepository

from .reports_status import CLIReportsStatus

DEFAULT_TEMPLATE_PATH = "template.xlsx"
DEFAULT_DATABASE_PATH = "transition_plan.db"

PathArg: TypeAlias = Annotated[Path, typer.Argument(help="Path to the file of folder of PDF student grades historic(s)")]
TemplateOption: TypeAlias = Annotated[Path, typer.Option(help="Path to the XLSX template")]
DatabaseOption: TypeAlias = Annotated[Path, typer.Option(help="Path to the SQLite subjects database")]

class TyperCLIHandler:
    _subject_repository: SubjectRepository

    _info_gateway: StudentInfoGateway
    _homologation_report_gateway: HomologationReportGateway
    _pending_subjects_report_gateway: PendingSubjectsReportGateway

    _homologable_subjects_service: HomologableSubjectsService
    _report_service: StudentReportService
    _pending_subjects_service: PendingSubjectsService

    _logger: Logger
    _app: typer.Typer

    def __init__(
        self,
        subject_repository: type[SubjectRepository],
        student_info_gateway: StudentInfoGateway,
        homologation_report_gateway: type[HomologationReportGateway],
        pending_subjects_report_gateway: PendingSubjectsReportGateway,
        logger: Logger
    ):
        self._subject_repository = subject_repository

        self._info_gateway = student_info_gateway
        self._homologation_report_gateway = homologation_report_gateway
        self._pending_subjects_report_gateway = pending_subjects_report_gateway

        self._logger = logger

        self._app = typer.Typer(
            help="Gather useful information from a USTA student grades historic file (in PDF format)",
            rich_markup_mode=None,
            add_completion=False
        )

        self._app.command(name="generate")(self._generate_reports)

    def run(self):
        self._app()

    def _generate_reports(
        self,
        path: PathArg,
        template: TemplateOption = DEFAULT_TEMPLATE_PATH,
        database: DatabaseOption = DEFAULT_DATABASE_PATH
    ):
        files_extracted_from_path = utils.resolve_path(path, "pdf")

        subject_repository = self._subject_repository(database, self._logger)
        
        self._homologable_subjects_service = HomologableSubjectsService(
            subject_repository,
            self._logger
        )

        self._pending_subjects_service = PendingSubjectsService(
            subject_repository,
            self._logger
        )

        self._report_service = StudentReportService(
            self._homologation_report_gateway(template),
            self._pending_subjects_report_gateway,
            self._logger
        )

        self._process_files(files_extracted_from_path)

    def _process_files(self, files: list[Path]):
        status = CLIReportsStatus(len(files))

        for file in files:

            self._logger.info(f"processing file {file}")

            student = self._info_gateway.extract_student_from(file)

            self._logger.info("generating homologation report")

            approved_subjects = self._homologable_subjects_service.suggest_subjects(student.grades)
            homologation_data = HomologationReportData.from_student(student, approved_subjects)

            homologation_report_result = self._report_service.generate_homologation_report(homologation_data)

            self._logger.info("generating pending subjects report")

            approved_codes = self._extract_codes_from_approved_subjects(approved_subjects)
            pending_subjects = self._pending_subjects_service.get_pending_subjects(approved_codes)

            pending_subjects_data = PendingSubjectsReportData.from_student(student, pending_subjects)

            pending_subjects_report_result = self._report_service.generate_pending_subjects_report(pending_subjects_data)

            self._logger.info("reports generated")

            status.add_finished_reports(student.name, [homologation_report_result, pending_subjects_report_result])

        status.stop()

        rich.print(f"[green]Reports generated at folders [yellow]{DEFAULT_HOMOLOGATION_REPORTS_DIR}[/yellow] and [yellow]{DEFAULT_PENDING_SUBJECTS_REPORTS_DIR}[/yellow][/green]")

    def _extract_codes_from_approved_subjects(self, subjects: list[ApprovedSubject]) -> list[SubjectCode]:
        return list(map(lambda approved: approved.target_subject.code, subjects))
