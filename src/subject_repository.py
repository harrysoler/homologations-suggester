from typing import Protocol

from entities import OldPensumSubject, NewPensumSubject

class ProjectRepository(Protocol):
    def find_homologable_subjects(subjects: list[OldPensumSubject]) -> list[NewPensumSubject]:
        ...

