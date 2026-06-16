from dataclasses import dataclass

from shared_types import SubjectCode, SubjectName, SubjectCredits, Semester

@dataclass(frozen=True)
class OldPensumSubject:
    """
    Subject of the old pensum (code may be the same for another new pensum
    subject)
    """
    code: SubjectCode
    name: SubjectName
    credits: SubjectCredits
    semester: Semester

    def __post_init__(self):
        if not self.code:
            raise ValueError("code must be a positive integer")

        if not self.name or not self.name.strip():
            raise ValueError("name must be a non-empty string")

        if self.credits is None:
            raise ValueError("credits must be a positive integer")

        if not (1 <= self.semester <= 10):
            raise ValueError("semester must be between 1 and 10")
