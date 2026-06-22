from dataclasses import dataclass

from student_info_gateway import StudentInfoGateway
from student_report_gateway import StudentReportGateway

@dataclass(frozen=True)
class StudentReportService:
    _info_gateway: StudentInfoGateway
    _report_gateway: StudentReportGateway
