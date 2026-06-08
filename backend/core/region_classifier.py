class RegionClassifier:

    def __init__(
        self,
        filesize,
        family="UNKNOWN"
    ):

        self.filesize = filesize
        self.family = family

        self.layout = (
            self._build_layout()
        )

    def _build_layout(
        self
    ):

        #
        # TOYOTA DENSO
        #
        if self.family == "TOYOTA":

            return {

                "boot": (
                    0,
                    0x1FFF
                ),

                "code": (
                    0x2000,
                    0x7FFF
                ),

                "calibration": (
                    0x8000,
                    self.filesize - 65
                ),

                "checksum": (
                    self.filesize - 64,
                    self.filesize - 1
                )
            }

        #
        # MITSUBISHI 4D56 / 4M41
        #
        elif self.family == "MITSUBISHI_4D56_4M41":

            return {

                "boot": (
                    0,
                    int(
                        self.filesize * 0.06
                    ) - 1
                ),

                "code": (
                    int(
                        self.filesize * 0.06
                    ),
                    int(
                        self.filesize * 0.50
                    )
                ),

                "calibration": (
                    int(
                        self.filesize * 0.50
                    ) + 1,
                    self.filesize - 65
                ),

                "checksum": (
                    self.filesize - 64,
                    self.filesize - 1
                )
            }

        #
        # MITSUBISHI 4N15
        #
        elif self.family == "MITSUBISHI_4N15":

            return {

                "boot": (
                    0,
                    int(
                        self.filesize * 0.06
                    ) - 1
                ),

                "code": (
                    int(
                        self.filesize * 0.06
                    ),
                    int(
                        self.filesize * 0.55
                    )
                ),

                "calibration": (
                    int(
                        self.filesize * 0.55
                    ) + 1,
                    self.filesize - 65
                ),

                "checksum": (
                    self.filesize - 64,
                    self.filesize - 1
                )
            }

        #
        # NISSAN
        #
        elif self.family == "NISSAN":

            return {

                "boot": (
                    0,
                    int(
                        self.filesize * 0.05
                    ) - 1
                ),

                "code": (
                    int(
                        self.filesize * 0.05
                    ),
                    int(
                        self.filesize * 0.45
                    )
                ),

                "calibration": (
                    int(
                        self.filesize * 0.45
                    ) + 1,
                    self.filesize - 65
                ),

                "checksum": (
                    self.filesize - 64,
                    self.filesize - 1
                )
            }

        #
        # GENERIC FALLBACK
        #
        return {

            "boot": (
                0,
                int(
                    self.filesize * 0.0625
                ) - 1
            ),

            "code": (
                int(
                    self.filesize * 0.0625
                ),
                int(
                    self.filesize * 0.55
                )
            ),

            "calibration": (
                int(
                    self.filesize * 0.55
                ) + 1,
                self.filesize - 65
            ),

            "checksum": (
                self.filesize - 64,
                self.filesize - 1
            )
        }

    def classify_regions(
        self,
        regions
    ):

        output = []

        for region in regions:

            item = dict(
                region
            )

            item[
                "classification"
            ] = self.classify_address(
                region["start"]
            )

            output.append(
                item
            )

        return output

    def classify_address(
        self,
        address
    ):

        if (

            self.layout["boot"][0]
            <= address
            <= self.layout["boot"][1]

        ):

            return "BOOT"

        if (

            self.layout["code"][0]
            <= address
            <= self.layout["code"][1]

        ):

            return "CODE"

        if (

            self.layout["calibration"][0]
            <= address
            <= self.layout["calibration"][1]

        ):

            return "CALIBRATION"

        if (

            self.layout["checksum"][0]
            <= address
            <= self.layout["checksum"][1]

        ):

            return "CHECKSUM"

        return "UNKNOWN"

    def get_layout(
        self
    ):

        return self.layout