from pathlib import Path
from typing import List

from export_strategies import CsvExportStrategy, TxtExportStrategy
from utils import APP_NAME
from app_paths import user_data_dir


class HistoryManager:

    def __init__(
            self,
            history_file="calculator_history.txt"
    ):

        self.path = self._resolve_path(history_file)

    def _resolve_path(self, filename: str) -> Path:
        candidate = Path(filename)
        if candidate.is_absolute():
            return candidate

        # Compatibility: prefer history file in current working directory if present.
        cwd_path = Path.cwd() / filename
        if cwd_path.exists():
            return cwd_path

        return user_data_dir(APP_NAME) / filename

    def read_history(self):

        if not self.path.exists():
            return []

        return self.path.read_text(encoding="utf-8").splitlines(keepends=True)

    def clear_history(self):

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("", encoding="utf-8")

    def export_txt(
            self,
            export_file="exports/history_export.txt"
    ):

        lines = self.read_history()
        target = self._resolve_export_path(export_file)
        TxtExportStrategy().export(lines, target)

    def export_csv(
            self,
            export_file="exports/history_export.csv"
    ):

        lines = self.read_history()
        target = self._resolve_export_path(export_file)
        CsvExportStrategy().export(lines, target)

    def _resolve_export_path(self, export_file: str) -> Path:
        path = Path(export_file)
        if path.is_absolute():
            return path
        # Keep exports in user data dir by default (works for .app bundles too).
        return user_data_dir(APP_NAME) / path

    def append_line(self, line: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(line)
