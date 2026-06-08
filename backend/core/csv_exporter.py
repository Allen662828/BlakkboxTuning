from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable


class CSVExporter:
    """Export simple tabular calibration results to CSV."""

    @staticmethod
    def _flatten_value(value: Any) -> str:
        if isinstance(value, (dict, list, tuple, set)):
            return repr(value)
        return "" if value is None else str(value)

    def export(self, rows: Iterable[dict], filename: str | Path) -> str:
        rows = list(rows)
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: self._flatten_value(v) for k, v in row.items()})

        return str(path)

    def export_report(self, report: dict[str, Any], filename: str | Path) -> str:
        flattened = []
        for key, value in report.items():
            flattened.append({"field": key, "value": self._flatten_value(value)})
        return self.export(flattened, filename)
