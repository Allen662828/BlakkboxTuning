class DeltaSafetyAnalyzer:

    def analyze(
        self,
        changes
    ):

        report = {

            "safe": True,

            "large_deltas": 0,

            "warnings": []
        }

        for change in changes:

            delta = abs(
                change["delta"]
            )

            if delta > 8:

                report[
                    "large_deltas"
                ] += 1

            if delta > 25:

                report[
                    "warnings"
                ].append({

                    "address":
                        change["address"],

                    "delta":
                        delta
                })

        if (

            report[
                "large_deltas"
            ]

            >

            500

        ):

            report[
                "safe"
            ] = False

        return report