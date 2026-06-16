import re
from collections.abc import Callable
from logging import Logger
from pathlib import Path

from pypdf import PdfReader

import utils
from shared_types import Grade, StudentGrades, StudentIdentification, SubjectCode
from student_info_gateway import StudentInfoGateway

STUDENT_NAME_REGEX = r"Estudiante[\s\n]+Identificaci.+n:\s+\d+\s+(.+?)(?:Código:)"
STUDENT_ID_REGEX = r"Identificaci.+n:\s+(\d+)"

REGISTRATION_STATUS_VALUES = ["Matriculado", "Repite", "vez"]

class PDFStudentInfoGateway(StudentInfoGateway):
    """
    Extracts students grades and core information from a Grades Historic PDF
    """

    _logger: Logger

    def __init__(self, logger: Logger, pdf_path: str):
        self._logger = logger

        if Path(pdf_path).suffix != ".pdf":
            raise ValueError(f"Unsupported file format: {pdf_path}")

        self._logger.debug("opening pdf file: %s", pdf_path)
        self._reader = PdfReader(pdf_path)
        self._text = " ".join(page.extract_text() for page in self._reader.pages)

    def get_name(self) -> str:
        match = re.search(STUDENT_NAME_REGEX, self._text)

        if match:
            student_name = match.group(1).strip()

            self._logger.debug("found student name: %s", student_name)

            return student_name

        raise ValueError("Could not extract student name from PDF")

    def get_identification(self) -> StudentIdentification:
        match = re.search(STUDENT_ID_REGEX, self._text)

        if match:
            return int(match.group(1))

        raise ValueError("Could not extract student identification from PDF")

    def get_graded_subjects(self) -> StudentGrades:
        raw_lines = self._text.split("\n")
        raw_subject_lines = self._extract_subjects_tables_content(raw_lines)

        cleaned_subject_lines = utils.flatten(list(map(utils.split_and_strip, raw_subject_lines)))
        raw_subjects = self._split_lines_by_subject(cleaned_subject_lines)

        # when converted to dict the last grade with the same key (subject code) wins
        subject_grades = dict(map(self._extract_subject, raw_subjects))

        self._logger.debug("found subject grades: %s", subject_grades)

        return subject_grades

    def _extract_subjects_tables_content(self, lines: list[str]) -> list[str]:
        table_prefixes = [index for index, item in enumerate(lines) if item in "Fall."]
        table_suffixes = [index for index, item in enumerate(lines) if item in "H:  Horas Semanales  C:  Créditos  S:  Sesiones  HS:  Horas  "]

        table_content_ranges = list(zip(table_prefixes, table_suffixes))

        if not table_content_ranges:
            return ValueError("Subjects table content not found")

        return utils.flatten(list(map(
            lambda range: lines[range[0] + 1:range[1]],
            table_content_ranges
        )))

    def _split_lines_by_subject(self, parts: list[str]) -> list[list[str]]:
        # where is every subject code
        subject_code_indexes = self._extract_subject_code_indexes(parts)

        # delimit ranges between subjects
        subject_index_ranges = utils.zip_items_in_shifted_pairs(subject_code_indexes)

        # add the last subject index range and a None to get the last index in the parts
        subject_index_ranges = subject_index_ranges + [(subject_code_indexes[-1], None)]

        return list(map(lambda range: parts[range[0]:range[1]], subject_index_ranges))

    def _extract_subject_code_indexes(self, parts: list[str]) -> list[int]:
        return [index for index, item in enumerate(parts) if self._is_a_subject_code(item)]

    def _is_a_subject_code(self, input: str) -> bool:
        return input.isdigit() and len(input) == 5

    def _extract_subject(self, parts: list[str]) -> tuple[SubjectCode, Grade] | None:
        # the first part is always the code
        subject_code = self._extract_subject_code_from(parts[0])

        if not subject_code:
            return None

        final_grade = self._extract_final_grade_from(parts)

        if not final_grade:
            return None

        return (subject_code, final_grade)

    def _extract_subject_code_from(self, input: str) -> SubjectCode | None:
        if input.isdigit() and len(input) == 5:
            return int(input)

        return None

    def _extract_final_grade_from(self, parts: list[str]) -> Grade | None:
        # remove subject code, credits, etc
        raw_subject_parts = self._remove_unnecesary_parts_from_raw_subject(parts)

        if not raw_subject_parts:
            return None

        # sometimes there is only left the final grade
        if len(raw_subject_parts) == 1:
            return float(raw_subject_parts[0])

        # locate where is the last percentage item and return final grade depending on that
        if '%' in raw_subject_parts[-2]:
            return float(raw_subject_parts[-1])

        if '%' in raw_subject_parts[-3]:
            return float(raw_subject_parts[-2])

        if '%' in raw_subject_parts[-4]:
            return float(raw_subject_parts[-2])

        return None

    def _remove_unnecesary_parts_from_raw_subject(self, parts: list[str]) -> list[str] | None:
        # get index where the item is "Matriculado" or "Repite"
        split_index = utils.search_index_by_any_match(REGISTRATION_STATUS_VALUES, parts)

        # the parts after columns "H" and "C"
        result = parts[split_index + 3:] if split_index else None

        # in the unfortunate case the pdf page is splitted in a row
        return utils.remove_last_str_items_until_digit_found(result)

    def _find_index_with_condition(self, condition: Callable[[str], bool], items: list[str]) -> int | None:
        return next(
            (index for index, item in enumerate(items) if condition(item)),
            None
        )
