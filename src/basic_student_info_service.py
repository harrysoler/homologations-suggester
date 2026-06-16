from dataclasses import dataclass

from student_info_gateway import StudentInfoGateway
from shared_types import StudentName, StudentIdentification

@dataclass(frozen=True)
class BasicStudentInfoService:
    _student_info_gateway: StudentInfoGateway

    def get_student_name(self) -> StudentName:
        return self._student_info_gateway.get_name()

    def get_student_identification(self) -> StudentIdentification:
        return self._student_info_gateway.get_identification()
