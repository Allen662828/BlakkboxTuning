class BoostStructureDetector:

    BOOST_SHAPES = {
        "16x16",
        "20x20",
        "24x24",
        "32x32"
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

        score = 0.0

        if shape in self.BOOST_SHAPES:
            score += 40

        if family == "BOOST":
            score += 40

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

        score += smooth_ratio * 15
        score += unique_ratio * 5

        classification = "UNKNOWN"

        if score >= 80:
            classification = "BOOST_PRIMARY"

        elif score >= 60:
            classification = "BOOST_SECONDARY"

        elif score >= 45:
            classification = "BOOST_CANDIDATE"

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
                "boost_classification"
            ] = result[
                "classification"
            ]

            item[
                "boost_score"
            ] = result[
                "score"
            ]

            output.append(
                item
            )

        output.sort(

            key=lambda x:
            x.get(
                "boost_score",
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

            "BOOST_PRIMARY": 0,
            "BOOST_SECONDARY": 0,
            "BOOST_CANDIDATE": 0,
            "UNKNOWN": 0
        }

        for table in tables:

            cls = table.get(
                "boost_classification",
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