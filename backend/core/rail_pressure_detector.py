class RailPressureDetector:

    RAIL_SHAPES = {
        "12x12",
        "16x16"
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

        if shape in self.RAIL_SHAPES:
            score += 40

        if family == "RAIL_PRESSURE":
            score += 50

        smooth_ratio = float(
            table.get(
                "smooth_ratio",
                0
            )
        )

        score += (
            smooth_ratio
            * 10
        )

        classification = "UNKNOWN"

        if score >= 80:
            classification = "RAIL_PRIMARY"

        elif score >= 60:
            classification = "RAIL_SECONDARY"

        elif score >= 40:
            classification = "RAIL_CANDIDATE"

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
                "rail_classification"
            ] = result[
                "classification"
            ]

            item[
                "rail_score"
            ] = result[
                "score"
            ]

            output.append(
                item
            )

        output.sort(

            key=lambda x:
            x.get(
                "rail_score",
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

            "RAIL_PRIMARY": 0,
            "RAIL_SECONDARY": 0,
            "RAIL_CANDIDATE": 0,
            "UNKNOWN": 0
        }

        for table in tables:

            cls = table.get(
                "rail_classification",
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