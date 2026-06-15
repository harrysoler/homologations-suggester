from typing import Protocol

from entities import OldPensumSubject, NewPensumSubject

class SubjectRepository(Protocol):
    def find_homologable_subject_for(subject: OldPensumSubject) -> NewPensumSubject:
        ...

