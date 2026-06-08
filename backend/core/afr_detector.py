class AFRDetector:

    def detect(
        self,
        tables
    ):

        output = []

        for table in tables:

            confidence = 0

            if table.get(
                "shape",
                ""
            ) == "SMOOTH":

                confidence += 30

            if table.get(
                "span",
                0
            ) >= 30:

                confidence += 40

            if table.get(
                "smooth_ratio",
                0
            ) >= 0.90:

                confidence += 30

            if confidence >= 75:

                table["family"] = (
                    "AFR"
                )

                table["confidence"] = (
                    confidence
                )

                output.append(
                    table
                )

        return output