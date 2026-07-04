import logging
from dataclasses import dataclass

from entities import HomologationReportData, PendingSubjectsReportData
from gateways import HomologationReportGateway, PendingSubjectsReportGateway
from shared_types import ReportGenerationResult


@dataclass(frozen=True)
class StudentReportService:
    _homologation_report_gateway: HomologationReportGateway
    _pending_subjects_report_gateway: PendingSubjectsReportGateway
    _logger: logging.Logger

    def generate_homologation_report(self, homologation_data: HomologationReportData) -> ReportGenerationResult:
        return self._homologation_report_gateway.generate_report(homologation_data)

    def generate_pending_subjects_report(self, pending_subjects_data: PendingSubjectsReportData) -> ReportGenerationResult:
        return self._pending_subjects_report_gateway.generate_report(pending_subjects_data)
