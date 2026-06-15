from dataclasses import dataclass

from subject_repository import SubjectRepository

@dataclass(frozen=True)
class SuggestSubjectsService:
    _subject_repository: SubjectRepository

    def __init__(self, subject_repository: SubjectRepository):
        self._subject_repository = subject_repository
