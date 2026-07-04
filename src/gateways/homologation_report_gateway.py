from typing import Protocol

from entities import HomologationReportData
from shared_types import ReportGenerationResult

class HomologationReportGateway(Protocol):
    """
    Defines the API for generation of homologation reports  
    """

    def generate_report(self, report: HomologationReportData) -> ReportGenerationResult:
        ...
