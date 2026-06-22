from dataclasses import dataclass

from student_info_gateway import StudentInfoGateway


@dataclass(frozen=True)
class HomologablesReportService:
    _student_info_gateway: StudentInfoGateway
