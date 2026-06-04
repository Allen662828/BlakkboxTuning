#!/usr/bin/env python3
"""BlakkboxTuning binary review utility.

Scope:
- Compare OEM and MOD binaries.
- Report changed bytes and contiguous clusters.
- Export human-readable and machine-readable summaries.
- Provide checksum-review placeholders for downstream tooling.

Non-scope:
- No tuning logic.
- No performance calibration generation.
- No map editing.
- No checksum patching.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class Cluster:
    start: int
    end: int
    length: int


@dataclass(frozen=True)
class ReviewStats:
    oem_path: str
    mod_path: str
    size_bytes: int
    size_match: bool
    changed_bytes: int
    changed_ratio: float
    cluster_count: int
    min_cluster: int
    max_cluster: int
    mean_cluster: float
    median_cluster: float
    first_change: int | None
    last_change: int | None
    entropy_oem: float
    entropy_mod: float
    checksum_notes: str


def read_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if not data:
        raise ValueError(f"Empty file: {path}")
    return data


def byte_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    ent = 0.0
    for count in counts.values():
        p = count / n
        ent -= p * math.log2(p)
    return ent


def diff_positions(oem: bytes, mod: bytes) -> List[int]:
    if len(oem) != len(mod):
        raise ValueError("Binary sizes differ; compare aligned files only.")
    return [i for i, (a, b) in enumerate(zip(oem, mod)) if a != b]


def build_clusters(positions: Sequence[int]) -> List[Cluster]:
    if not positions:
        return []
    clusters: List[Cluster] = []
    start = prev = positions[0]
    for pos in positions[1:]:
        if pos == prev + 1:
            prev = pos
            continue
        clusters.append(Cluster(start=start, end=prev, length=prev - start + 1))
        start = prev = pos
    clusters.append(Cluster(start=start, end=prev, length=prev - start + 1))
    return clusters


def median(values: Sequence[int]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    mid = len(s) // 2
    if len(s) % 2:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def format_hex(value: int | None) -> str:
    return "-" if value is None else f"0x{value:08X}"


def write_csv(path: Path, clusters: Sequence[Cluster]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "start_hex", "end_hex", "start_dec", "end_dec", "length"])
        for idx, c in enumerate(clusters, start=1):
            writer.writerow([idx, f"0x{c.start:08X}", f"0x{c.end:08X}", c.start, c.end, c.length])


def write_md(path: Path, stats: ReviewStats, clusters: Sequence[Cluster]) -> None:
    lines = []
    lines.append("# Binary Review Report")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- OEM: `{stats.oem_path}`")
    lines.append(f"- MOD: `{stats.mod_path}`")
    lines.append(f"- Size: `{stats.size_bytes}` bytes")
    lines.append(f"- Size match: `{stats.size_match}`")
    lines.append(f"- Changed bytes: `{stats.changed_bytes}`")
    lines.append(f"- Changed ratio: `{stats.changed_ratio:.6f}`")
    lines.append(f"- Clusters: `{stats.cluster_count}`")
    lines.append(f"- First change: `{format_hex(stats.first_change)}`")
    lines.append(f"- Last change: `{format_hex(stats.last_change)}`")
    lines.append(f"- OEM entropy: `{stats.entropy_oem:.6f}`")
    lines.append(f"- MOD entropy: `{stats.entropy_mod:.6f}`")
    lines.append("")
    lines.append("## Cluster Statistics")
    lines.append(f"- Minimum cluster length: `{stats.min_cluster}`")
    lines.append(f"- Maximum cluster length: `{stats.max_cluster}`")
    lines.append(f"- Mean cluster length: `{stats.mean_cluster:.3f}`")
    lines.append(f"- Median cluster length: `{stats.median_cluster:.3f}`")
    lines.append("")
    lines.append("## Checksum Review Notes")
    lines.append(stats.checksum_notes)
    lines.append("")
    lines.append("## Clusters")
    if not clusters:
        lines.append("No byte differences detected.")
    else:
        for idx, c in enumerate(clusters, start=1):
            lines.append(f"{idx}. `0x{c.start:08X}` - `0x{c.end:08X}` ({c.length} bytes)")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze OEM vs MOD binary differences.")
    parser.add_argument("oem", type=Path, help="OEM binary path")
    parser.add_argument("mod", type=Path, help="MOD binary path")
    parser.add_argument("--outdir", type=Path, default=Path("reports"), help="Output directory")
    args = parser.parse_args()

    oem = read_bytes(args.oem)
    mod = read_bytes(args.mod)

    if len(oem) != len(mod):
        raise SystemExit(f"Size mismatch: OEM={len(oem)} MOD={len(mod)}")

    positions = diff_positions(oem, mod)
    clusters = build_clusters(positions)
    cluster_lengths = [c.length for c in clusters]

    first_change = positions[0] if positions else None
    last_change = positions[-1] if positions else None

    notes = (
        "Checksum validity is not determined by this script. "
        "Use the ECU-specific checksum tool or flashing software to confirm stored-vs-calculated checksum equality."
    )

    stats = ReviewStats(
        oem_path=str(args.oem),
        mod_path=str(args.mod),
        size_bytes=len(oem),
        size_match=True,
        changed_bytes=len(positions),
        changed_ratio=(len(positions) / len(oem)) if oem else 0.0,
        cluster_count=len(clusters),
        min_cluster=min(cluster_lengths) if cluster_lengths else 0,
        max_cluster=max(cluster_lengths) if cluster_lengths else 0,
        mean_cluster=(sum(cluster_lengths) / len(cluster_lengths)) if cluster_lengths else 0.0,
        median_cluster=median(cluster_lengths),
        first_change=first_change,
        last_change=last_change,
        entropy_oem=byte_entropy(oem),
        entropy_mod=byte_entropy(mod),
        checksum_notes=notes,
    )

    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "bin_review.json").write_text(json.dumps(asdict(stats), indent=2), encoding="utf-8")
    write_csv(args.outdir / "modified_regions.csv", clusters)
    write_md(args.outdir / "bin_review.md", stats, clusters)

    print(json.dumps(asdict(stats), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
