class RailLimitDetector:

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

                128,
                256
            ]:

                confidence += 40

            if table.get(
                "span",
                0
            ) >= 50:

                confidence += 30

            if table.get(
                "smooth_ratio",
                0
            ) >= 0.85:

                confidence += 30

            if confidence >= 75:

                table["family"] = (
                    "RAIL_LIMIT"
                )

                table["confidence"] = (
                    confidence
                )

                output.append(
                    table
                )

        return output