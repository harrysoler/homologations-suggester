from pathlib import Path

from entities import PendingSubjectsReportData
from gateways import PendingSubjectsReportGateway
from shared_types import ReportGenerationResult

REPORTS_DIR = Path("pending_subject_reports")


class TXTPendingSubjectsReportGateway(PendingSubjectsReportGateway):
    def generate_report(self, data: PendingSubjectsReportData) -> ReportGenerationResult:
        REPORTS_DIR.mkdir(exist_ok=True)

        safe_name = data.name.lower().replace(' ', '_')
        filename = f"pending_subjects_{safe_name}.txt"
        filepath = REPORTS_DIR / filename

        lines = [
            data.name.title(),
            f"Identificación: {data.identification}",
            "",
            f"{'Código':<10}{'Nombre':<45}{'Créditos':<10}{'Semestre':<10}",
            "-" * 75,
        ]

        for subject in data.pending_subjects:
            lines.append(
                f"{subject.code:<10}{subject.name:<45}{subject.credits:<10}{subject.semester:<10}"
            )

        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(filepath)
