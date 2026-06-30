from pathlib import Path

from rich.progress import Progress


class CLIProgressBar:
    _bar: Progress
    _task_id: int

    def __init__(self, file: Path):
        self._bar = Progress()
        self._task_id = self._bar.add_task(f"{file}", total=5)

        self._bar.start()

    def advance(self, description: str):
        self._bar.update(self._task_id, description=description, advance=1)

    def end(self):
        self._bar.stop()
        
