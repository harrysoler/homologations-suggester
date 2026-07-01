from dataclasses import dataclass

from .new_subject import NewPensumSubject
from .old_subject import OldPensumSubject
from shared_types import Grade

@dataclass(frozen=True)
class ApprovedSubject:
    """
    Aggregate of an approved homologation between subjects of the old and new
    pensum
    """
    origin_subject: OldPensumSubject
    grade: Grade

    target_subject: NewPensumSubject

    def __post_init__(self):
        if self.origin_subject is None:
            raise ValueError("origin_subject must not be None")

        if self.target_subject is None:
            raise ValueError("target_subject must not be None")

