import logging
import sqlite3
from pathlib import Path

import click

import utils
from adapter.cli.files_processor import CLIFilesProcessor
from adapter.student_report_gateway.xlsx import XLSXStudentReportGateway
from adapter.subject_repository.sqlite import SQLiteSubjectRepository

LOGGING_FORMAT = "%(message)s"

DEFAULT_TEMPLATE_PATH = "template.xlsx"
DEFAULT_DATABASE_PATH = "transition_plan.db"

def setup_subject_repository(db_path: str, logger: logging.Logger) -> sqlite3.Connection:
    try:
        return SQLiteSubjectRepository(Path(db_path), logger)
    except sqlite3.OperationalError as error:
        raise click.ClickException(f"Error creating SQLite repository: {error}")

def setup_logger(verbose: bool) -> logging.Logger:
    file_handler = logging.FileHandler("debug.log", mode="w")
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="[%X]"))

    logger = logging.getLogger("file")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

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

    files_processor = CLIFilesProcessor(
        subject_repository,
        report_gateway,
        logger
    )

    files_processor.process_files(files_extracted_from_path)

if __name__ == "__main__":
    main()
