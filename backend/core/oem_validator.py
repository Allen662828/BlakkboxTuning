from __future__ import annotations

from typing import Iterable


class OEMValidator:
    def validate(self, original, modified, modified_regions):
        size_match = len(original) == len(modified)

        regions = sorted(
            (
                int(region.get("start", 0)),
                int(region.get("end", -1))
            )
            for region in (modified_regions or [])
        )

        cluster_integrity = True
        offset_drift_detected = False

        last_end = -1
        for start, end in regions:
            if start < 0 or end < start:
                cluster_integrity = False
                break
            if start <= last_end:
                cluster_integrity = False
                break
            last_end = end

        untouched_bytes_preserved = True
        if size_match and cluster_integrity:
            modified_mask = [False] * len(original)
            for start, end in regions:
                for idx in range(max(0, start), min(len(modified_mask), end + 1)):
                    modified_mask[idx] = True

            for idx, (o, m) in enumerate(zip(original, modified)):
                if not modified_mask[idx] and o != m:
                    untouched_bytes_preserved = False
                    break
        else:
            untouched_bytes_preserved = False

        oem_preservation_pass = (
            size_match
            and untouched_bytes_preserved
            and not offset_drift_detected
            and cluster_integrity
        )

        return {
            "size_match": size_match,
            "untouched_bytes_preserved": untouched_bytes_preserved,
            "offset_drift_detected": offset_drift_detected,
            "cluster_integrity": cluster_integrity,
            "oem_preservation_pass": oem_preservation_pass,
        }
