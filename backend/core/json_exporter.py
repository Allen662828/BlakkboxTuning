from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JSONExporter:
    """Export calibration reports as JSON."""

    def export(self, report: Any, filename: str | Path) -> str:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=4, ensure_ascii=False)

        return str(path)

    def dumps(self, report: Any) -> str:
        return json.dumps(report, indent=4, ensure_ascii=False)
