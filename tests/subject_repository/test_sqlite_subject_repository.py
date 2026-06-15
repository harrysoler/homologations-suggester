import os
import sqlite3
import pytest

from adapter.subject_repository.sqlite.sqlite_subject_repository import (
    SQLiteSubjectRepository,
)
from entities import OldPensumSubject, NewPensumSubject

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DDL_PATH = os.path.join(BASE_DIR, "transition_plan_ddl.sql")

def _create_test_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = OFF")

    with open(DDL_PATH, "r") as f:
        ddl_sql = f.read()
    conn.executescript(ddl_sql)

    conn.commit()
    return conn


@pytest.fixture()
def repository():
    conn = _create_test_db()
    repo = SQLiteSubjectRepository(conn)
    yield repo
    conn.close()


@pytest.fixture()
def old_subjects():
    return {
        96110: OldPensumSubject(code=96110, name="CALCULO DIFERENCIAL", credits=3, semester=1),
        41112: OldPensumSubject(code=41112, name="INTRODUCCION A LA PROGRAMACION", credits=3, semester=1),
        96111: OldPensumSubject(code=96111, name="ALGEBRA LINEAL", credits=3, semester=2),
        95125: OldPensumSubject(code=95125, name="INGLES I", credits=2, semester=1),
        95108: OldPensumSubject(code=95108, name="FILOSOFIA INSTITUCIONAL", credits=2, semester=1),
        41111: OldPensumSubject(code=41111, name="INTRODUCCION A LA INGENIERIA DE SISTEMAS", credits=3, semester=1),
        96113: OldPensumSubject(code=96113, name="CALCULO INTEGRAL", credits=3, semester=2),
        83007: OldPensumSubject(code=83007, name="METODOS NUMERICOS", credits=3, semester=5),
        30107: OldPensumSubject(code=30107, name="PROBABILIDAD Y ESTADISTICA", credits=2, semester=6),
        95127: OldPensumSubject(code=95127, name="INGLES II", credits=2, semester=2),
        96181: OldPensumSubject(code=96181, name="PROGRAMACION ORIENTADA A OBJETOS", credits=3, semester=2),
        96500: OldPensumSubject(code=96500, name="BASES DE DATOS", credits=3, semester=2),
        96200: OldPensumSubject(code=96200, name="CALCULO VECTORIAL", credits=3, semester=3),
        40748: OldPensumSubject(code=40748, name="DESARROLLO EMPRESARIAL", credits=3, semester=5),
        96112: OldPensumSubject(code=96112, name="FISICA MECANICA", credits=3, semester=3),
        95128: OldPensumSubject(code=95128, name="INGLES III", credits=2, semester=3),
    }


class TestFindHomologableSubjectFor:
    def test_returns_new_subject_when_homologable_exists(self, repository, old_subjects):
        old = old_subjects[96110]
        result = repository.find_homologable_subject_for(old)

        assert result is not None
        assert result.code == 11701
        assert result.credits == 3
        assert result.semester == 1

    def test_returns_self_mapped_subject(self, repository, old_subjects):
        old = old_subjects[96113]
        result = repository.find_homologable_subject_for(old)

        assert result is not None
        assert result.code == 96113

    def test_returns_none_when_no_homologable(self, repository):
        old = OldPensumSubject(code=99999, name="MATERIA INEXISTENTE", credits=3, semester=1)
        result = repository.find_homologable_subject_for(old)

        assert result is None

    def test_returns_correct_subject_for_all_homologable_mappings(self, repository, old_subjects):
        expected_mappings = {
            96110: 11701,
            41112: 31160,
            96111: 96103,
            95125: 15650,
            95108: 10240,
            41111: 41111,
            96113: 96113,
            83007: 30115,
            30107: 91504,
            95127: 15651,
            96181: 96181,
            96500: 96500,
            96200: 96115,
            40748: 40748,
            96112: 96112,
            95128: 15652,
        }

        for old_code, expected_new_code in expected_mappings.items():
            old = old_subjects[old_code]
            result = repository.find_homologable_subject_for(old)

            assert result is not None, f"Expected homologable for old subject code {old_code}"
            assert result.code == expected_new_code, (
                f"Old subject {old_code}: expected new code {expected_new_code}, got {result.code}"
            )

    def test_returns_new_subject_with_correct_attributes(self, repository, old_subjects):
        old = old_subjects[96181]
        result = repository.find_homologable_subject_for(old)

        assert result is not None
        assert isinstance(result, NewPensumSubject)
        assert result.code == 96181
        assert result.name == "PROGRAMACION ORIENTADA A OBJETOS"
        assert result.credits == 3
        assert result.semester == 2

    def test_returns_new_subject_for_elective_mapping(self, repository, old_subjects):
        old = old_subjects[83007]
        result = repository.find_homologable_subject_for(old)

        assert result is not None
        assert result.code == 30115

    def test_returns_new_subject_for_language_mapping(self, repository, old_subjects):
        old = old_subjects[95125]
        result = repository.find_homologable_subject_for(old)

        assert result is not None
        assert result.code == 15650
