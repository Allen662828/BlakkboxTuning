class VNTDetector:

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
            ) in [

                256,
                400
            ]:

                confidence += 40

            if table.get(
                "smooth_ratio",
                0
            ) >= 0.85:

                confidence += 40

            if table.get(
                "span",
                0
            ) >= 40:

                confidence += 20

            if confidence >= 75:

                table["family"] = (
                    "VNT"
                )

                table["confidence"] = (
                    confidence
                )

                output.append(
                    table
                )

        return output