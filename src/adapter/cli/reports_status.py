from pathlib import Path

from rich.console import Console
from rich.progress import Progress


class CLIReportsStatus:
    _console: Console
    _progress: Progress

    _total_reports: int

    def __init__(self, total_reports: int):
        self._total_reports = total_reports

        self._console = Console(log_time=False, log_path=False)

        self._progress = Progress(console=self._console)

        self._task_id = self._progress.add_task("Generating reports", total=total_reports)

        self._progress.start()

    def add_finished_reports(self, student_name: str, reports_path: list[Path]):
        self._console.log(f"[green]✓[/green] {student_name}: [grey30]{", ".join(reports_path)}[/grey30]")

        self._progress.update(self._task_id, advance=1)

    def stop(self):
        self._progress.stop()
        
