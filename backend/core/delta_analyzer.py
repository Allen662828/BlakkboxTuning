class DeltaAnalyzer:

    def analyze(
        self,
        changes
    ):

        total = len(
            changes
        )

        histogram = {

            "0-5": 0,
            "6-8": 0,
            "9-16": 0,
            "17-32": 0,
            "33-64": 0,
            "65+": 0
        }

        for change in changes:

            delta = abs(
                change["delta"]
            )

            if delta <= 5:

                histogram["0-5"] += 1

            elif delta <= 8:

                histogram["6-8"] += 1

            elif delta <= 16:

                histogram["9-16"] += 1

            elif delta <= 32:

                histogram["17-32"] += 1

            elif delta <= 64:

                histogram["33-64"] += 1

            else:

                histogram["65+"] += 1

        risk = 0

        if total:

            risk = round(

                (
                    histogram["65+"]
                    +
                    histogram["33-64"]
                )

                * 100

                / total,

                2
            )

        severity = "MILD"

        if risk > 20:
            severity = "MODERATE"

        if risk > 40:
            severity = "AGGRESSIVE"

        if risk > 60:
            severity = "OVER_MODIFIED"

        return {

            "severity":
                severity,

            "risk_level":
                (
                    "HIGH"
                    if risk > 40
                    else "LOW"
                ),

            "risk_score":
                risk,

            "total_changed":
                total,

            "histogram":
                histogram
        }