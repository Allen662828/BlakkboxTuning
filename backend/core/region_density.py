class RegionDensity:

    def analyze(
        self,
        classified_regions
    ):

        boot_bytes = 0
        code_bytes = 0
        calibration_bytes = 0
        checksum_bytes = 0

        total_bytes = 0

        for region in classified_regions:

            length = region.get(
                "length",
                0
            )

            total_bytes += length

            classification = (
                region.get(
                    "classification",
                    "UNKNOWN"
                )
            )

            if classification == "BOOT":

                boot_bytes += length

            elif classification == "CODE":

                code_bytes += length

            elif classification == "CALIBRATION":

                calibration_bytes += length

            elif classification == "CHECKSUM":

                checksum_bytes += length

        if total_bytes == 0:

            return {

                "boot_density": 0.0,
                "code_density": 0.0,
                "calibration_density": 0.0,
                "checksum_density": 0.0,

                "boot_bytes": 0,
                "code_bytes": 0,
                "calibration_bytes": 0,
                "checksum_bytes": 0,

                "total_modified_bytes": 0
            }

        return {

            "boot_density": round(
                boot_bytes * 100 / total_bytes,
                2
            ),

            "code_density": round(
                code_bytes * 100 / total_bytes,
                2
            ),

            "calibration_density": round(
                calibration_bytes * 100 / total_bytes,
                2
            ),

            "checksum_density": round(
                checksum_bytes * 100 / total_bytes,
                2
            ),

            "boot_bytes":
                boot_bytes,

            "code_bytes":
                code_bytes,

            "calibration_bytes":
                calibration_bytes,

            "checksum_bytes":
                checksum_bytes,

            "total_modified_bytes":
                total_bytes
        }