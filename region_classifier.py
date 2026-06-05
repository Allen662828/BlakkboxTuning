"""
region_classifier.py

ROM region classification engine.

Purpose:
- Identify whether modified bytes belong to:
    BOOT
    CODE
    CALIBRATION
    CHECKSUM
    UNKNOWN

This layer does NOT identify maps.
It identifies ROM areas only.
"""


class RegionClassifier:

    def __init__(self, filesize):

        self.filesize = filesize

        self.boot_start = 0
        self.boot_end = 0

        self.code_start = 0
        self.code_end = 0

        self.cal_start = 0
        self.cal_end = 0

        self.checksum_start = 0
        self.checksum_end = 0

        self._detect_layout()

    def _detect_layout(self):

        #
        # SH7058
        # 1MB
        #

        if self.filesize == 1048576:

            self.boot_start = 0x000000
            self.boot_end = 0x00FFFF

            self.code_start = 0x010000
            self.code_end = 0x08CC0C

            self.cal_start = 0x08CC0D
            self.cal_end = 0x0FFFBF

            self.checksum_start = 0x0FFFC0
            self.checksum_end = 0x0FFFFF

            return

        #
        # SH7059
        # 2MB
        #

        if self.filesize == 2097152:

            self.boot_start = 0x000000
            self.boot_end = 0x01FFFF

            self.code_start = 0x020000
            self.code_end = 0x120000

            self.cal_start = 0x120001
            self.cal_end = 0x1FFF7F

            self.checksum_start = 0x1FFF80
            self.checksum_end = 0x1FFFFF

            return

        #
        # Generic fallback
        #

        self.boot_start = 0
        self.boot_end = 0

        self.code_start = 0
        self.code_end = int(self.filesize * 0.55)

        self.cal_start = self.code_end + 1
        self.cal_end = self.filesize - 129

        self.checksum_start = self.filesize - 128
        self.checksum_end = self.filesize - 1

    def classify(self, start_offset, end_offset):

        if (
            start_offset >= self.boot_start
            and
            end_offset <= self.boot_end
        ):
            return "BOOT"

        if (
            start_offset >= self.code_start
            and
            end_offset <= self.code_end
        ):
            return "CODE"

        if (
            start_offset >= self.cal_start
            and
            end_offset <= self.cal_end
        ):
            return "CALIBRATION"

        if (
            start_offset >= self.checksum_start
            and
            end_offset <= self.checksum_end
        ):
            return "CHECKSUM"

        return "UNKNOWN"

    def get_layout(self):

        return {
            "boot": [
                self.boot_start,
                self.boot_end
            ],

            "code": [
                self.code_start,
                self.code_end
            ],

            "calibration": [
                self.cal_start,
                self.cal_end
            ],

            "checksum": [
                self.checksum_start,
                self.checksum_end
            ]
        }

    def classify_region_dict(self, region):

        start = region["start"]
        end = region["end"]

        #
        # Compatibility with older
        # hex-string region formats
        #

        if isinstance(start, str):
            start = int(start, 16)

        if isinstance(end, str):
            end = int(end, 16)

        region["classification"] = (
            self.classify(
                start,
                end
            )
        )

        return region

    def classify_regions(self, regions):

        classified = []

        for region in regions:

            classified.append(
                self.classify_region_dict(
                    region
                )
            )

        return classified