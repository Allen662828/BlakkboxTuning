class DTCDetector:

    def detect(
        self,
        clusters
    ):

        output = []

        for cluster in clusters:

            length = cluster.get(
                "length",
                0
            )

            if length < 8:
                continue

            output.append({

                "start":
                    cluster["start"],

                "end":
                    cluster["end"],

                "length":
                    length,

                "suspected_dtc":
                    True,

                "confidence":
                    50
            })

        return output