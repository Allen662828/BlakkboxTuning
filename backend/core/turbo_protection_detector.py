class TurboProtectionDetector:

    def detect(
        self,
        tables
    ):

        output = []

        for table in tables:

            confidence = 0

            if table.get(
                "size",
                0
            ) >= 256:

                confidence += 40

            if table.get(
                "span",
                0
            ) >= 70:

                confidence += 30

            if table.get(
                "smooth_ratio",
                0
            ) >= 0.80:

                confidence += 30

            if confidence >= 80:

                table["family"] = (
                    "TURBO_PROTECTION"
                )

                table["confidence"] = (
                    confidence
                )

                output.append(
                    table
                )

        return output