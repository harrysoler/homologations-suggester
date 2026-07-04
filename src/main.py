import logging

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
