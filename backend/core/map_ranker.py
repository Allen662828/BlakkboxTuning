class MapRanker:

    def rank_tables(
        self,
        tables,
        calibration_clusters,
        calibration_base
    ):

        ranked = []

        for table in tables:

            absolute_start = (
                calibration_base
                +
                table["address"]
            )

            absolute_end = (
                absolute_start
                +
                table["size"]
                -
                1
            )

            overlap_bytes = 0

            touched_clusters = 0

            for cluster in calibration_clusters:

                overlap_start = max(
                    absolute_start,
                    cluster["start"]
                )

                overlap_end = min(
                    absolute_end,
                    cluster["end"]
                )

                if overlap_end >= overlap_start:

                    overlap = (
                        overlap_end
                        -
                        overlap_start
                        +
                        1
                    )

                    overlap_bytes += overlap

                    touched_clusters += 1

            if table["size"] > 0:

                overlap_ratio = round(

                    overlap_bytes
                    * 100
                    /
                    table["size"],

                    2
                )

            else:

                overlap_ratio = 0

            smooth_ratio = (
                table.get(
                    "smooth_ratio",
                    0
                )
            )

            score = round(

                (
                    overlap_ratio
                    * 0.70
                )

                +

                (
                    smooth_ratio
                    * 100
                    * 0.30
                ),

                2
            )

            ranked.append({

                "address":
                    table["address"],

                "absolute_start":
                    absolute_start,

                "absolute_end":
                    absolute_end,

                "size":
                    table["size"],

                "overlap_bytes":
                    overlap_bytes,

                "overlap_ratio":
                    overlap_ratio,

                "touched_clusters":
                    touched_clusters,

                "smooth_ratio":
                    smooth_ratio,

                "score":
                    score
            })

        ranked.sort(

            key=lambda x:
                x["score"],

            reverse=True
        )

        return ranked