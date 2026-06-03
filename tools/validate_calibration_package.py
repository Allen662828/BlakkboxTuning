#!/usr/bin/env python3
"""Validate Blakkbox calibration package manifests.

This script intentionally validates package discipline only. It does not tune,
smooth, alter, or approve ECU calibration values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "sw_id",
    "ecu",
    "engine",
    "transmission",
    "original_file",
    "mod_file",
    "final_file",
    "checksum_method",
    "checksum_correction_offset",
    "review",
]

REQUIRED_REVIEW = [
    "smoke_control",
    "fuel_knock",
    "combustion_stability",
    "surface_quality",
    "structural_integrity",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: manifest must be a JSON object")
    return data


def require_nonempty_string(data: dict[str, Any], key: str, path: Path) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{path}: `{key}` must be a non-empty string")


def validate_manifest(path: Path) -> None:
    data = load_manifest(path)
    base = path.parent

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            raise SystemExit(f"{path}: missing required field `{key}`")

    for key in REQUIRED_TOP_LEVEL:
        if key != "review":
            require_nonempty_string(data, key, path)

    review = data["review"]
    if not isinstance(review, dict):
        raise SystemExit(f"{path}: `review` must be an object")

    for key in REQUIRED_REVIEW:
        value = review.get(key)
        if not isinstance(value, str) or len(value.strip()) < 20:
            raise SystemExit(
                f"{path}: `review.{key}` must be a meaningful review statement"
            )

    if data["sw_id"] not in str(path):
        raise SystemExit(f"{path}: manifest path should include SW ID `{data['sw_id']}`")

    original = (base / data["original_file"]).resolve()
    mod = (base / data["mod_file"]).resolve()
    final = (base / data["final_file"]).resolve()

    for file_path, label in [(original, "original_file"), (mod, "mod_file"), (final, "final_file")]:
        if not file_path.exists():
            raise SystemExit(f"{path}: `{label}` does not exist: {file_path}")
        if file_path.stat().st_size == 0:
            raise SystemExit(f"{path}: `{label}` is empty: {file_path}")

    sizes = {original.stat().st_size, mod.stat().st_size, final.stat().st_size}
    if len(sizes) != 1:
        raise SystemExit(f"{path}: original, mod, and final files must be the same size")

    original_bytes = original.read_bytes()
    mod_bytes = mod.read_bytes()
    final_bytes = final.read_bytes()

    if original_bytes == mod_bytes:
        raise SystemExit(f"{path}: MOD is identical to ORIGINAL; package appears stock")

    final_vs_original = sum(a != b for a, b in zip(original_bytes, final_bytes))
    if final_vs_original == 0:
        raise SystemExit(f"{path}: FINAL is identical to ORIGINAL; package appears stock")

    final_vs_mod = sum(a != b for a, b in zip(mod_bytes, final_bytes))
    if final_vs_mod > 64:
        raise SystemExit(
            f"{path}: FINAL differs from MOD by {final_vs_mod} bytes; "
            "large post-MOD changes require a separate reviewed delta report"
        )

    checksum_method = data["checksum_method"].lower()
    if "sum8" in checksum_method:
        original_sum = sum(original_bytes) & 0xFF
        final_sum = sum(final_bytes) & 0xFF
        if original_sum != final_sum:
            raise SystemExit(
                f"{path}: sum8 mismatch, original=0x{original_sum:02X}, "
                f"final=0x{final_sum:02X}"
            )

    print(f"OK {path}")
    print(f"  original_sha256={sha256(original)}")
    print(f"  mod_sha256={sha256(mod)}")
    print(f"  final_sha256={sha256(final)}")
    print(f"  final_vs_original_changed_bytes={final_vs_original}")
    print(f"  final_vs_mod_changed_bytes={final_vs_mod}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", nargs="+", type=Path)
    args = parser.parse_args()
    for manifest in args.manifests:
        validate_manifest(manifest)


if __name__ == "__main__":
    main()
