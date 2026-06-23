import logging
import sqlite3
from pathlib import Path

import click
from rich.logging import RichHandler

import utils
from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from adapter.student_report_gateway.xlsx import XLSXStudentReportGateway
from adapter.subject_repository.sqlite import SQLiteSubjectRepository
from entities import Student
from gateways import StudentReportGateway
from services import HomologableSubjectsService, StudentReportService
from subject_repository import SubjectRepository

LOGGING_FORMAT = "%(message)s"

DEFAULT_TEMPLATE_PATH = "template.xlsx"
DEFAULT_DATABASE_PATH = "transition_plan.db"

def setup_subject_repository(db_path: str, logger: logging.Logger) -> sqlite3.Connection:
    try:
        return SQLiteSubjectRepository(Path(db_path), logger)
    except sqlite3.OperationalError as error:
        raise click.ClickException(f"Error creating SQLite repository: {error}")

def setup_logger(verbose: bool) -> logging.Logger:
    log_file = Path(__file__).resolve().parent.parent / "debug.log"

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="[%X]"))

    console_handler = RichHandler()
    console_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level="DEBUG" if verbose else "INFO",
        format=LOGGING_FORMAT,
        datefmt="[%X]",
        handlers=[file_handler, console_handler]
    )

    return logging.getLogger("rich")

def build_student_from_file(file: Path, subject_repository: SubjectRepository, logger: logging.Logger) -> Student:
    logger.info("    parsing pdf text")

    info_gateway = PDFStudentInfoGateway(logger, file)

    logger.info("    obtaining homologable subjects")

    homologable_subjects = HomologableSubjectsService(
        subject_repository,
        info_gateway,
        logger
    ).suggest_subjects()

    return Student(
        info_gateway.get_name(),
        info_gateway.get_identification(),
        homologable_subjects
    )

def process_files(subject_repository: SubjectRepository, report_gateway: StudentReportGateway, files: list[Path], logger: logging.Logger):
    for file in files:
        logger.info(f"processing file {file}")

        student = build_student_from_file(file, subject_repository, logger)

        logger.info("    generating report")

        report_result = StudentReportService(
            report_gateway,
            logger
        ).generate_report(student)

        logger.info(f"    report generated at {report_result}")

@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--template", "-t", type=click.Path(exists=True, dir_okay=False), default=DEFAULT_TEMPLATE_PATH, help="Path to the XLSX template file.")
@click.option("--database", "-db", type=click.Path(exists=True, dir_okay=False), default=DEFAULT_DATABASE_PATH, help="Path to the SQLite subjects database.")
@click.option("--verbose", "-v", is_flag=True, help="Enable DEBUG logging level.")
def main(pdf_path: str, template: str, database: str, verbose: bool):
    logger = setup_logger(verbose)

    files_extracted_from_path = utils.resolve_path(pdf_path, "pdf")

    subject_repository = setup_subject_repository(DEFAULT_DATABASE_PATH, logger)
    report_gateway = XLSXStudentReportGateway(template)

    process_files(
        subject_repository,
        report_gateway,
        files_extracted_from_path,
        logger,
    )

if __name__ == "__main__":
    main()

