import logging
import sqlite3
from pathlib import Path

import click

from adapter.cli import TyperCLIHandler
from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from adapter.student_report_gateway.xlsx import XLSXStudentReportGateway
from adapter.subject_repository.sqlite import SQLiteSubjectRepository

LOGGING_FORMAT = "%(message)s"

def setup_logger() -> logging.Logger:
    file_handler = logging.FileHandler("debug.log", mode="w")
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="[%X]"))

    logger = logging.getLogger("file")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

def setup_subject_repository(db_path: str, logger: logging.Logger) -> sqlite3.Connection:
    try:
        return SQLiteSubjectRepository(Path(db_path), logger)
    except sqlite3.OperationalError as error:
        raise click.ClickException(f"Error creating SQLite repository: {error}")


def main():
    logger = setup_logger()

    cli = TyperCLIHandler(
        SQLiteSubjectRepository,
        XLSXStudentReportGateway,
        PDFStudentInfoGateway(logger),
        logger
    )

    cli.run()

if __name__ == "__main__":
    main()
