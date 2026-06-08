class DeltaShapeValidator:

    def validate(
        self,
        maps
    ):

        summary = {

            "valid": 0,
            "invalid": 0
        }

        for table in maps:

            smooth = table.get(
                "smooth_ratio",
                0
            )

            if smooth >= 0.75:

                summary["valid"] += 1

            else:

                summary["invalid"] += 1

        return summary