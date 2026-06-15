import re
from pypdf import PdfReader

from typing import TypeAlias, Mapping

Grade: TypeAlias = float
SubjectCode: TypeAlias = int
StudentGrades: TypeAlias = Mapping[SubjectCode, Grade]

def main():
    reader = PdfReader("./tests/pdf_gateway/examples/second_semester_historic_example.pdf")

    all_text = " ".join(page.extract_text() for page in reader.pages)

    lines = all_text.split("\n")

    def extract_subjects_tables_content(lines: list[str]) -> list[str]:
        table_prefixes = [index for index, item in enumerate(lines) if item in "Fall."]
        table_suffixes =[index for index, item in enumerate(lines) if item in "H:  Horas Semanales  C:  Créditos  S:  Sesiones  HS:  Horas  "]

        table_content_ranges = list(zip(table_prefixes, table_suffixes))

        if not table_content_ranges:
            return ValueError("Subjects table content not found")

        return flatten(list(map(
            lambda range: lines[range[0] + 1:range[1]],
            table_content_ranges
        )))

    def split_and_strip(input: str) -> list[str]:
        return list(map(str.strip, input.split()))

    def flatten(items: list[list[str]]) -> list[str]:
        return [item for sublist in items for item in sublist]

    def separate_in_subject_sections(parts: list[str]) -> list[list[str]]:
        subject_code_indexes = extract_subject_code_indexes(parts)

        subject_index_ranges = zip_in_shifted_pairs(subject_code_indexes)

        # add the last subject index range and a None to get the last index in the parts
        subject_index_ranges = subject_index_ranges + [(subject_code_indexes[-1], None)]

        return list(map(lambda range: parts[range[0]:range[1]], subject_index_ranges))

    def extract_subject_code_indexes(parts: list[str]) -> list[int]:
        return [index for index, item in enumerate(parts) if is_a_subject_code(item)]
        
    def is_a_subject_code(input: str) -> bool:
        return input.isdigit() and len(input) == 5

    def zip_in_shifted_pairs(items: list[int]) -> list[tuple[int, int]]:
        return list(zip(items, items[1:]))

    def extract_subject(parts: list[str]) -> tuple[SubjectCode, Grade] | None:
        # the first part is always the code
        subject_code = extract_subject_code(parts[0])

        if not subject_code:
            return None

        final_grade = extract_final_grade(parts)

        # if not final_grade:
        #     return None

        return (subject_code, final_grade)

    def extract_subject_code(input: str) -> SubjectCode | None:
        if input.isdigit() and len(input) == 5:
            return int(input)

        return None

    def extract_final_grade(raw_subject_parts: list[str]) -> Grade | None:
        # print(raw_subject_parts)

        raw_subject_parts = remove_unnecesary_parts(raw_subject_parts)

        if not raw_subject_parts:
            return None

        # sometimes there is only left the final grade
        if len(raw_subject_parts) == 1:
            return float(raw_subject_parts[0])

        if '%' in raw_subject_parts[-2]:
            return float(raw_subject_parts[-1])

        if '%' in raw_subject_parts[-3]:
            return float(raw_subject_parts[-2])

        return None

    def remove_unnecesary_parts(parts: list[str]) -> list[str] | None:
        # get index where the item is "Matriculado" or "Repite"
        split_index = search_index_by_any_match(["Matriculado","Repite"], parts)

        # return the parts after columns "H" and "C"
        return parts[split_index + 3:] if split_index else None

    lines = extract_subjects_tables_content(lines)

    parts = flatten(list(map(split_and_strip, lines)))

    raw_subject_sections = separate_in_subject_sections(parts)

    subjects = dict(map(extract_subject, raw_subject_sections))

    print(subjects)

def search_index_by_any_match(matches: list[str] | str, items: list[str]) -> int | None:
    return next(
        (index for index, item in enumerate(items) if item in matches),
        None
    )

if __name__ == "__main__":
    main()
