from typing import Protocol

from entities import PendingSubjectsReportData
from shared_types import ReportGenerationResult

class PendingSubjectsReportGateway(Protocol):
    """
    Defines the API for generation of pending subjects reports  
    """

    def generate_report(self, report: PendingSubjectsReportData) -> ReportGenerationResult:
        ...
