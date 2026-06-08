class SmokeLimiterDetector:

    SMOKE_SHAPES = {

        "16x20",
        "20x20",
        "24x24"
    }

    def classify_map(
        self,
        table
    ):

        shape = table.get(
            "shape",
            "UNKNOWN"
        )

        family = table.get(
            "family",
            "UNKNOWN"
        )

        score = 0

        if shape in self.SMOKE_SHAPES:
            score += 35

        if family == "SMOKE":
            score += 45

        smooth_ratio = float(
            table.get(
                "smooth_ratio",
                0
            )
        )

        unique_ratio = float(
            table.get(
                "unique_ratio",
                0
            )
        )

        score += (
            smooth_ratio
            * 10
        )

        score += (
            unique_ratio
            * 10
        )

        classification = "UNKNOWN"

        if score >= 80:
            classification = "SMOKE_PRIMARY"

        elif score >= 60:
            classification = "SMOKE_SECONDARY"

        elif score >= 45:
            classification = "SMOKE_CANDIDATE"

        return {

            "classification":
                classification,

            "score":
                round(score, 2)
        }

    def classify_tables(
        self,
        tables
    ):

        output = []

        for table in tables:

            result = self.classify_map(
                table
            )

            item = dict(table)

            item[
                "smoke_classification"
            ] = result[
                "classification"
            ]

            item[
                "smoke_score"
            ] = result[
                "score"
            ]

            output.append(
                item
            )

        output.sort(

            key=lambda x:
            x.get(
                "smoke_score",
                0
            ),

            reverse=True
        )

        return output

    def summarize(
        self,
        tables
    ):

        summary = {

            "SMOKE_PRIMARY": 0,
            "SMOKE_SECONDARY": 0,
            "SMOKE_CANDIDATE": 0,
            "UNKNOWN": 0
        }

        for table in tables:

            cls = table.get(
                "smoke_classification",
                "UNKNOWN"
            )

            summary[cls] = (
                summary.get(
                    cls,
                    0
                )
                + 1
            )

        return summary