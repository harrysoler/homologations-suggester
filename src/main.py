import logging
import sqlite3
import os
from pathlib import Path

from rich.logging import RichHandler

from adapter.subject_repository.sqlite import SQLiteSubjectRepository
from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from suggest_subject_service import SuggestSubjectsService

LOGGING_FORMAT = "%(message)s"

PATH_PREFIX = "/media/data/teach/intersemestral_2026/plan_de_transicion/historicos_tercer_semestre"

def main():
    logging.basicConfig(
        level="INFO",
        format=LOGGING_FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()]
    )

    logger = logging.getLogger("rich")

    for filename in os.listdir(PATH_PREFIX):
        full_path = os.path.join(PATH_PREFIX, filename)

        if not os.path.isfile(full_path):
            continue

        if Path(full_path).suffix != ".pdf":
            continue

        student_info_gateway = PDFStudentInfoGateway(logger, full_path)

        conn = sqlite3.connect("transition_plan.db")

        subject_repository = SQLiteSubjectRepository(conn, logger)
    
        suggest_subjects_service = SuggestSubjectsService(subject_repository, student_info_gateway, logger)

        suggest_subjects_service.suggest_homologable_subjects()
    

if __name__ == "__main__":
    main()
