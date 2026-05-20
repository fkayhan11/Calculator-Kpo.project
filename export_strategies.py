import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class TxtExportStrategy:
    def export(self, lines: List[str], target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(lines), encoding="utf-8")


@dataclass(frozen=True)
class CsvExportStrategy:
    header: str = "Operation"

    def export(self, lines: List[str], target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([self.header])
            for line in lines:
                writer.writerow([line.strip()])
