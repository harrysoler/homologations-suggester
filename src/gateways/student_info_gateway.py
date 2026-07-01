from typing import Protocol
from pathlib import Path

from entities import Student

class StudentInfoGateway(Protocol):
    """
    Extractor of student information
    """
    def extract_student_from(self, path: Path) -> Student:
        ...
