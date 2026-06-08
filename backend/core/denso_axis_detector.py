class DensoAxisDetector:

    def detect(
        self,
        axes
    ):

        detected = []

        for axis in axes:

            span = axis.get(
                "span",
                0
            )

            confidence = 0

            if span >= 50:

                confidence += 40

            if axis.get(
                "length",
                0
            ) >= 16:

                confidence += 30

            if axis.get(
                "end",
                0
            ) > axis.get(
                "start",
                0
            ):

                confidence += 30

            if confidence >= 70:

                detected.append({

                    "address":
                        axis["address"],

                    "confidence":
                        confidence,

                    "length":
                        axis["length"]
                })

        return detected