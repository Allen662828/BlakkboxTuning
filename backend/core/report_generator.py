from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class ReportGenerator:
    """Generate a compact human-readable analysis report."""

    def generate(self, analysis: dict[str, Any]) -> dict[str, Any]:
        swid = analysis.get("swid", {}) or {}
        processor = analysis.get("processor_analysis", {}) or {}
        map_summary = analysis.get("map_ranking_summary", {}) or {}
        validation = analysis.get("oem_validation", {}) or {}

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "swid": swid,
            "rom_size": processor.get("rom_size", 0),
            "changed_regions": processor.get("changed_regions", 0),
            "cluster_count": processor.get("cluster_count", 0),
            "detected_maps": map_summary.get("detected_maps", 0),
            "oem_safe": bool(validation.get("oem_preservation_pass", False)),
            "status": "COMPLETE",
        }

    def render_text(self, report: dict[str, Any]) -> str:
        lines = [
            "DENSO ROM REPORT",
            f"Generated: {report.get('generated_at', '')}",
            f"Status: {report.get('status', 'UNKNOWN')}",
            f"ROM size: {report.get('rom_size', 0)} bytes",
            f"Changed regions: {report.get('changed_regions', 0)}",
            f"Clusters: {report.get('cluster_count', 0)}",
            f"Detected maps: {report.get('detected_maps', 0)}",
            f"OEM safe: {report.get('oem_safe', False)}",
        ]
        return "\n".join(lines)
