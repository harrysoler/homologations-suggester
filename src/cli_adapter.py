import logging
from pathlib import Path

import click

import utils
from adapter.homologation_xlsx_fill import HomologationXLSXFillService
from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from basic_student_info_service import BasicStudentInfoService
from entities import Student
from student_info_gateway import StudentInfoGateway
from subject_repository import SubjectRepository
from suggest_subject_service import SuggestSubjectsService


class CLIAdapter:
    _subject_repository: SubjectRepository
    _xlsx_fill_service: HomologationXLSXFillService
    _logger: logging.Logger

    def __init__(self, subject_repository: SubjectRepository, xlsx_fill_service: HomologationXLSXFillService, logger: logging.Logger):
        self._subject_repository = subject_repository
        self._xlsx_fill_service = xlsx_fill_service
        self._logger = logger

    def process_path(self, path: str):
        resolved_path = self._setup_path(path)

        # is a file or a list of files
        if isinstance(resolved_path, list):
            for file in resolved_path:
                self._process_pdf(file)
        else:
            self._process_pdf(resolved_path)

    def _setup_path(self, path: str) -> Path | list[Path]:
        try:
            return utils.resolve_path(path, "pdf")
        except ValueError as error:
            raise click.ClickException(f"Reading path: {error}")

    def _process_pdf(self, file_path: str):
        student_info_gateway = PDFStudentInfoGateway(self._logger, file_path)

        student = self._build_student_from(student_info_gateway)

        self._xlsx_fill_service.fill(student)

    def _build_student_from(self, student_info_gateway: StudentInfoGateway) -> Student:
        basic_info_service = BasicStudentInfoService(student_info_gateway)

        suggest_subjects_service = SuggestSubjectsService(
            self._subject_repository,
            student_info_gateway,
            self._logger
        )

        return Student(
            basic_info_service.get_student_name(),
            basic_info_service.get_student_identification(),
            suggest_subjects_service.suggest_homologable_subjects()
        )
