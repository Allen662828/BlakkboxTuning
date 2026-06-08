class CalibrationConfidence:

    def calculate(
        self,
        maps
    ):

        if not maps:

            return {

                "score": 0,
                "level": "NONE"
            }

        score = 0

        score += min(
            len(maps) * 4,
            60
        )

        confidence = min(
            score,
            100
        )

        if confidence >= 85:

            level = "HIGH"

        elif confidence >= 60:

            level = "MEDIUM"

        elif confidence >= 30:

            level = "LOW"

        else:

            level = "VERY_LOW"

        return {

            "score":
                confidence,

            "level":
                level,

            "map_count":
                len(maps)
        }