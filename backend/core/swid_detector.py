class SWIDDetector:

    PROFILES = {

        "TOYOTA": [
            "89663-"
        ],

        "MITSUBISHI_4D56_4M41": [
            "H11",
            "H12",
            "H13",
            "H14",
            "H15",
            "H16",
            "H17",
            "H18",
            "H19"
        ],

        "MITSUBISHI_4N15": [
            "H1A",
            "H1B",
            "H1C",
            "CST"
        ],

        "NISSAN": [
            "E30",
            "E31",
            "E51",
            "E63"
        ]
    }

    def detect(
        self,
        filename
    ):

        filename = str(
            filename
        ).upper()

        for family, patterns in self.PROFILES.items():

            for pattern in patterns:

                if pattern in filename:

                    return {

                        "detected": True,
                        "family": family,
                        "pattern": pattern
                    }

        return {

            "detected": False,
            "family": "UNKNOWN",
            "pattern": None
        }