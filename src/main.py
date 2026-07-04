import logging

from adapter.cli import TyperCLIHandler
from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from adapter.homologation_report_gateway.xlsx import XLSXHomologationReportGateway
from adapter.subject_repository.sqlite import SQLiteSubjectRepository
from adapter.pending_subjects_report_gateway.txt import TXTPendingSubjectsReportGateway

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
        PDFStudentInfoGateway(logger),
        XLSXHomologationReportGateway,
        TXTPendingSubjectsReportGateway(),
        logger
    )

    cli.run()

if __name__ == "__main__":
    main()
