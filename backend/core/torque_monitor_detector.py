class TorqueMonitorDetector:

    def detect(
        self,
        tables
    ):

        output = []

        for table in tables:

            shape = table.get(
                "shape",
                ""
            )

            size = table.get(
                "size",
                0
            )

            confidence = 0

            if shape == "TORQUE":

                confidence += 50

            if size in [
                256,
                400,
                512
            ]:

                confidence += 30

            if table.get(
                "span",
                0
            ) > 60:

                confidence += 20

            if confidence >= 70:

                table["family"] = (
                    "TORQUE_MONITOR"
                )

                table["confidence"] = (
                    confidence
                )

                output.append(
                    table
                )

        return output