import re
from collections.abc import Callable
from logging import Logger
from pathlib import Path

from pypdf import PdfReader

import utils
from shared_types import (
    Grade,
    StudentGrades,
    StudentIdentification,
    StudentName,
    SubjectCode,
)
from student_info_gateway import StudentInfoGateway

STUDENT_NAME_REGEX = r"Estudiante[\s\n]+Identificaci.+n:\s+\d+\s+(.+?)(?:Código:)"
STUDENT_ID_REGEX = r"Identificaci.+n:\s+(\d+)"

REGISTRATION_STATUS_VALUES = ["Matriculado", "vez", "Repite"]

class PDFStudentInfoGateway(StudentInfoGateway):
    """
    Extracts students grades and core information from a Grades Historic PDF
    """

    _logger: Logger

    def __init__(self, logger: Logger, pdf_path: str):
        self._logger = logger

        if Path(pdf_path).suffix != ".pdf":
            raise ValueError(f"Unsupported file format: {pdf_path}")

        self._logger.info("opening pdf file: %s", pdf_path)
        self._reader = PdfReader(pdf_path)
        self._text = " ".join(page.extract_text() for page in self._reader.pages)

    def get_name(self) -> StudentName:
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

        self._logger.debug("got raw text: %s", self._text)

        # split the text by breaklines and spaces
        raw_words = utils.flatten(text.split(' ') for text in self._text.split('\n'))
        self._logger.debug("got raw words: %s", input)

        raw_subjects = self._separate_words_by_subject(raw_words)
        self._logger.debug("got raw subjects: %s", raw_subjects)
        
        # when converted to dict the last grade with the same key (subject code) wins
        subject_grades = dict(map(self._extract_subject, raw_subjects))
        self._logger.debug("found subject grades: %s", subject_grades)

        return subject_grades

    def _separate_words_by_subject(self, input: list[str]) -> list[list[str]]:
        raw_subject_lines = self._extract_subjects_tables_content(input)

        self._logger.debug("got raw subject lines: %s", raw_subject_lines)

        # cleaned_subject_lines = utils.flatten(list(map(utils.split_and_strip, raw_subject_lines)))
        cleaned_subject_lines = list(map(str.strip, raw_subject_lines))

        self._logger.debug("got cleaned subject lines: %s", cleaned_subject_lines)

        return self._split_lines_by_subject(cleaned_subject_lines)
         
    def _extract_subjects_tables_content(self, lines: list[str]) -> list[str]:
        table_prefixes = [index for index, item in enumerate(lines) if item == "Fall."]
        table_suffixes = [index for index, item in enumerate(lines) if item == "H:"]

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
        self._logger.debug("extracting subject from: %s", parts)

        # the first part is always the code
        subject_code = self._extract_subject_code_from(parts[0])

        if not subject_code:
            self._logger.debug("subject code not found")
            return None

        final_grade = self._extract_final_grade_from(parts)

        if final_grade is None:
            self._logger.debug("subject grade not found")
            return None

        result = (subject_code, final_grade)

        return result

    def _extract_subject_code_from(self, input: str) -> SubjectCode | None:
        if input.isdigit() and len(input) == 5:
            return int(input)

        return None

    def _extract_final_grade_from(self, parts: list[str]) -> Grade | None:
        # remove subject code, credits, etc
        raw_subject_parts = self._remove_unnecesary_parts_from_raw_subject(parts)

        self._logger.debug("extracting grade from: %s", raw_subject_parts)

        if not raw_subject_parts:
            return None

        # sometimes there is only left the final grade
        if len(raw_subject_parts) == 1:
            return float(raw_subject_parts[0])

        #locate where is the final grade based on empty items in the list
        if raw_subject_parts[-1] != "":
            return float(raw_subject_parts[-2])

        if raw_subject_parts[-2] == "":
            return float(raw_subject_parts[-3])

        return None

    def _remove_unnecesary_parts_from_raw_subject(self, parts: list[str]) -> list[str] | None:
        # get index where the item is "Matriculado" or "Repite"
        split_index = utils.search_index_by_any_match(REGISTRATION_STATUS_VALUES, parts)

        if not split_index:
            return None

        # the parts after columns "H" and "C"
        result = parts[split_index + 3:]

        # in the unfortunate case the pdf page is splitted in a row
        result = utils.remove_last_str_items_until_digit_or_empty_found(result)

        return result

    def _find_index_with_condition(self, condition: Callable[[str], bool], items: list[str]) -> int | None:
        return next(
            (index for index, item in enumerate(items) if condition(item)),
            None
        )
