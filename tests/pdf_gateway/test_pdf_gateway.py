import pytest
import logging

from adapter.student_info_gateway.pdf import PDFStudentInfoGateway
from shared_types import StudentGrades

PDF_FIXTURES = {
    "example": {
        "path": "./tests/pdf_gateway/examples/first_semester_historic_example.pdf",
        "name": "ALBA JIMENEZ SARA",
        "identification": 1097188339,
        "subjects": {
            11711: 4.2,
            41111: 4.8,
            41112: 3.9,
            10240: 4.4,
            95125: 4.0,
            99101: 4.6,
            96110: 2.7,
            95127: 4.0,
            95083: 4.2,
        },
    },
    "example_2": {
        "path": "tests/pdf_gateway/examples/second_semester_historic_example.pdf",
        "name": "GALLO CASTAÑEDA JUAN ALEJANDRO",
        "identification": 1057979941,
        "subjects": {
            11711: 4.0,
            41111: 4.0,
            41112: 3.4,
            10240: 4.3,
            95125: 4.0,
            99102: 4.9,
            96110: 3.0,
            15135: 4.6,
            95127: 4.0,
            95128: 4.0,
        },
    },
    "example_3": {
        "path": "tests/pdf_gateway/examples/first_semester_historic_example_2.pdf",
        "name": "GALVIS RODRIGUEZ SERGIO ANDRES",
        "identification": 1095307185,
        "subjects": {
            11711: 3.9,
            41111: 4.9,
            41112: 4.3,
            10240: 4.6,
            95125: 4.0,
            99101: 4.9,
            96110: 4.2,
            95127: 4.0,
            95128: 4.0,
        },
    },
    "example_4": {
        "path": "tests/pdf_gateway/examples/first_semester_historic_example_3.pdf",
        "name": "RINCON ABRIL EDITH JUANITA",
        "identification": 1050609542,
        "subjects": {
            11711: 4.3,
            41111: 4.6,
            41112: 4.2,
            10240: 4.6,
            95125: 4.0,
            99101: 3.9,
            96110: 4.1,
            95082: 4.0,
            96300: 4.5,
            96501: 4.5,
        },
    },
}


@pytest.fixture(params=list(PDF_FIXTURES.keys()))
def pdf_gateway(request):
    """Fixture that returns a PDFStudentInfoGateway and expected data tuple."""
    fixture_name = request.param

    mock_logger = logging.getLogger("test")
    mock_logger.handlers = []

    fixture = PDF_FIXTURES[fixture_name]
    gateway = PDFStudentInfoGateway(mock_logger, fixture["path"])

    return gateway, fixture

def test_get_name(pdf_gateway):
    gateway, data = pdf_gateway
    assert gateway.get_name() == data["name"]

def test_get_identification(pdf_gateway):
    gateway, data = pdf_gateway
    assert gateway.get_identification() == data["identification"]

def test_get_graded_subjects(pdf_gateway):
    gateway, data = pdf_gateway

    subjects = gateway.get_graded_subjects()
    expected: StudentGrades = data["subjects"]

    for code, expected_grade in expected.items():
        assert subjects[code] == expected_grade, (
            f"Subject {code}: expected {expected_grade}, got {subjects.get(code)}"
        )
