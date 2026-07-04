from logging import Logger
from pathlib import Path
from typing import Annotated, TypeAlias

import typer

import utils
from gateways import StudentInfoGateway, HomologationReportGateway
from services import HomologableSubjectsService, StudentReportService
from subject_repository import SubjectRepository

from .reports_status import CLIReportsStatus

DEFAULT_TEMPLATE_PATH = "template.xlsx"
DEFAULT_DATABASE_PATH = "transition_plan.db"

PathArg: TypeAlias = Annotated[Path, typer.Argument(help="Path to the file of folder of PDF student grades historic(s)")]
TemplateOption: TypeAlias = Annotated[Path, typer.Option(help="Path to the XLSX template")]
DatabaseOption: TypeAlias = Annotated[Path, typer.Option(help="Path to the SQLite subjects database")]

class TyperCLIHandler:
    _subject_repository: SubjectRepository
    _report_gateway: HomologationReportGateway
    _info_gateway: StudentInfoGateway
    _logger: Logger
    _app: typer.Typer

    def __init__(
        self,
        subject_repository: type[SubjectRepository],
        student_report_gateway: HomologationReportGateway,
        student_info_gateway: StudentInfoGateway,
        logger: Logger
    ):
        self._subject_repository = subject_repository
        self._report_gateway = student_report_gateway
        self._info_gateway = student_info_gateway

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

        homologable_subjects_service = HomologableSubjectsService(
            self._subject_repository(database, self._logger),
            self._logger
        )

        report_service = StudentReportService(
            self._report_gateway(template),
            homologable_subjects_service,
            self._logger
        )

        self._process_files(files_extracted_from_path, report_service)

    def _process_files(self, files: list[Path], report_service: StudentReportService):
        status = CLIReportsStatus(len(files))

        for file in files:

            self._logger.info(f"processing file {file}")

            student = self._info_gateway.extract_student_from(file)

            self._logger.info("    generating report")

            report_result = report_service.generate_report_from(student)

            self._logger.info(f"    report generated at {report_result}")

            status.add_finished_report(student.name, report_result)

        status.stop()
