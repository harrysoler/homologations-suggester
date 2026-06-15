import sqlite3

from subject_repository import SubjectRepository
from entities import OldPensumSubject, NewPensumSubject


class SQLiteSubjectRepository(SubjectRepository):
    def __init__(self, db_connection: sqlite3.Connection):
        self._connection = db_connection

    def find_homologable_subject_for(self, subject: OldPensumSubject) -> NewPensumSubject | None:
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
        cursor.execute(query, (subject.code,))
        row = cursor.fetchone()

        if row is None:
            return None

        return NewPensumSubject(
            code=row["code"],
            name=row["name"],
            credits=row["credits"],
            semester=row["semester"],
        )
