import sqlite3
from logging import Logger
from pathlib import Path

from entities import NewPensumSubject, OldPensumSubject
from subject_repository import SubjectRepository


class SQLiteSubjectRepository(SubjectRepository):
    _connection: sqlite3.Connection
    _logger: Logger

    def __init__(self, db_path: Path, logger: Logger):
        self._connection = sqlite3.connect(db_path)
        self._logger = logger

    def find_old_subject_by_code(self, subject_code: int) -> OldPensumSubject | None:
        query = """
            SELECT code, name, credits, semester
            FROM old_curriculum_subject
            WHERE code = ?
        """

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(query, (subject_code,))
        row = cursor.fetchone()

        if row is None:
            self._logger.debug("old pensum subject %s not found", subject_code)
            return None

        return OldPensumSubject(
            code=row["code"],
            name=row["name"],
            credits=row["credits"],
            semester=row["semester"],
        )

    def find_new_subject_by_code(self, subject_code: int) -> NewPensumSubject | None:
        query = """
            SELECT code, name, credits, semester
            FROM new_curriculum_subject
            WHERE code = ?
        """

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(query, (subject_code,))
        row = cursor.fetchone()

        if row is None:
            self._logger.debug("new pensum subject %s not found", subject_code)
            return None

        return NewPensumSubject(
            code=row["code"],
            name=row["name"],
            credits=row["credits"],
            semester=row["semester"],
        )

    def find_homologable_subject_for(self, old_subject_code: int) -> NewPensumSubject | None:
        query = """
            SELECT
                n.code,
                n.name,
                n.credits,
                n.semester
            FROM homologable h
            JOIN new_curriculum_subject n ON n.code = h.new_subject_code
            WHERE h.old_subject_code = ?
        """

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(query, (old_subject_code,))
        row = cursor.fetchone()

        if row is None:
            return None

        return NewPensumSubject(
            code=row["code"],
            name=row["name"],
            credits=row["credits"],
            semester=row["semester"],
        )
