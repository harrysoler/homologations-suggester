from dataclasses import dataclass

from entities import OldPensumSubject, NewPensumSubject

@dataclass(frozen=True)
class ApprovedSubject:
    """
    Aggregate of an approved homologation between subjects of the old and new
    pensum
    """
    origin_subject: OldPensumSubject
    destination_subject: NewPensumSubject

    def __post_init__(self):
        if self.origin_subject is None:
            raise ValueError("origin_subject must not be None")

        if self.destination_subject is None:
            raise ValueError("destination_subject must not be None")

