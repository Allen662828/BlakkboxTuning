class MapSimilarityEngine:

    def compare(
        self,
        map_a,
        map_b
    ):

        data_a = map_a.get(
            "data",
            []
        )

        data_b = map_b.get(
            "data",
            []
        )

        if not data_a or not data_b:

            return 0

        matches = 0

        total = min(

            len(data_a),
            len(data_b)
        )

        for a, b in zip(
            data_a,
            data_b
        ):

            if abs(a - b) <= 2:

                matches += 1

        return round(

            matches
            * 100
            / total,

            2
        )