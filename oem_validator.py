"""
oem_validator.py

OEM Preservation Validator

Purpose:
- Verify untouched bytes remain identical
- Verify ROM sizes match
- Verify no offset drift
- Verify modification clustering quality
- Verify OEM preservation
"""


class OEMValidator:

    def validate(
        self,
        original,
        modified,
        regions
    ):

        report = {

            "size_match": False,
            "untouched_bytes_preserved": False,
            "offset_drift_detected": False,
            "cluster_integrity": False,
            "oem_preservation_pass": False
        }

        #
        # Size check
        #

        report["size_match"] = (
            len(original)
            ==
            len(modified)
        )

        #
        # Offset drift
        #

        report[
            "offset_drift_detected"
        ] = self.detect_offset_drift(
            original,
            modified
        )

        #
        # Untouched byte validation
        #

        report[
            "untouched_bytes_preserved"
        ] = self.verify_untouched_bytes(
            original,
            modified,
            regions
        )

        #
        # Cluster validation
        #

        report[
            "cluster_integrity"
        ] = self.validate_clusters(
            regions
        )

        report[
            "oem_preservation_pass"
        ] = (

            report["size_match"]

            and

            not report[
                "offset_drift_detected"
            ]

            and

            report[
                "untouched_bytes_preserved"
            ]

            and

            report[
                "cluster_integrity"
            ]
        )

        return report

    def detect_offset_drift(
        self,
        original,
        modified
    ):

        if len(original) != len(modified):

            return True

        return False

    def verify_untouched_bytes(
        self,
        original,
        modified,
        regions
    ):

        modified_map = set()

        for region in regions:

            start = region["start"]
            end = region["end"]

            for addr in range(
                start,
                end + 1
            ):

                modified_map.add(addr)

        for addr in range(
            len(original)
        ):

            if addr in modified_map:
                continue

            if (
                original[addr]
                !=
                modified[addr]
            ):
                return False

        return True

    def validate_clusters(
        self,
        regions
    ):

        if not regions:
            return True

        previous_end = -1

        for region in regions:

            if (
                region["start"]
                <
                previous_end
            ):

                return False

            previous_end = (
                region["end"]
            )

        return True