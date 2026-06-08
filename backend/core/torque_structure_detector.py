class TorqueStructureDetector:

    """
    Heuristic torque-structure classifier for DENSO diesel ROM analysis.

    Purpose:
    - Rank calibration tables that resemble torque-related structures.
    - Distinguish torque-like maps from generic limiters and boost tables.
    - Use shape, smoothness, overlap, and local delta density.
    """

    TORQUE_SHAPES = {
        "10x10",
        "11x11",
        "12x12",
        "16x16",
        "20x20",
        "24x24",
        "32x32"
    }

    LIMITER_SHAPES = {
        "8x8",
        "10x10",
        "12x12",
        "16x16"
    }

    BOOST_SHAPES = {
        "16x16",
        "20x20",
        "24x24"
    }

    def classify_map(
        self,
        table,
        overlapping_clusters=None
    ):

        overlapping_clusters = overlapping_clusters or []

        shape = table.get(
            "shape",
            "UNKNOWN"
        )

        family = table.get(
            "family",
            "UNKNOWN"
        )

        overlap_bytes = 0

        overlap_ratio = 0.0

        score = 0.0

        if shape in self.TORQUE_SHAPES:

            score += 35.0

        elif shape in self.LIMITER_SHAPES:

            score += 15.0

        if family == "TORQUE":

            score += 35.0

        elif family == "BOOST":

            score += 20.0

        elif family == "LIMITER":

            score += 10.0

        smooth_ratio = float(
            table.get(
                "smooth_ratio",
                0.0
            )
        )

        unique_ratio = float(
            table.get(
                "unique_ratio",
                0.0
            )
        )

        score += smooth_ratio * 20.0
        score += unique_ratio * 10.0

        overlap_bytes = int(
            table.get(
                "overlap_bytes",
                0
            )
        )

        size = int(
            table.get(
                "size",
                0
            )
        )

        if size > 0:

            overlap_ratio = round(
                overlap_bytes / size,
                4
            )

            score += overlap_ratio * 20.0

        if overlapping_clusters:

            longest_cluster = max(
                overlapping_clusters,
                key=lambda x: x.get(
                    "length",
                    0
                )
            )

            cluster_length = int(
                longest_cluster.get(
                    "length",
                    0
                )
            )

            if cluster_length >= 256:

                score += 10.0

            elif cluster_length >= 128:

                score += 5.0

        if shape == "16x16" and family == "TORQUE":
            score += 10.0

        if shape == "20x20" and family == "TORQUE":
            score += 8.0

        if shape == "24x24" and family == "TORQUE":
            score += 6.0

        classification = "UNKNOWN"

        if score >= 85.0:

            classification = "TORQUE_PRIMARY"

        elif score >= 70.0:

            classification = "TORQUE_SECONDARY"

        elif score >= 55.0:

            classification = "TORQUE_CANDIDATE"

        return {

            "classification":
                classification,

            "score":
                round(
                    score,
                    2
                ),

            "shape":
                shape,

            "family":
                family,

            "overlap_bytes":
                overlap_bytes,

            "overlap_ratio":
                overlap_ratio
        }

    def classify_tables(
        self,
        tables,
        clusters=None
    ):

        clusters = clusters or []

        output = []

        for table in tables:

            table_start = int(
                table.get(
                    "absolute_start",
                    table.get(
                        "address",
                        0
                    )
                )
            )

            table_end = int(
                table.get(
                    "absolute_end",
                    table_start + table.get(
                        "size",
                        0
                    ) - 1
                )
            )

            overlapping_clusters = []

            for cluster in clusters:

                cluster_start = int(
                    cluster.get(
                        "start",
                        0
                    )
                )

                cluster_end = int(
                    cluster.get(
                        "end",
                        0
                    )
                )

                if (
                    table_start <= cluster_end
                    and table_end >= cluster_start
                ):

                    overlapping_clusters.append(
                        cluster
                    )

            result = self.classify_map(
                table,
                overlapping_clusters
            )

            updated_table = dict(
                table
            )

            updated_table["torque_classification"] = (
                result["classification"]
            )

            updated_table["torque_score"] = (
                result["score"]
            )

            updated_table["torque_overlap_ratio"] = (
                result["overlap_ratio"]
            )

            updated_table["torque_overlap_bytes"] = (
                result["overlap_bytes"]
            )

            output.append(
                updated_table
            )

        output.sort(
            key=lambda x: (
                x.get(
                    "torque_score",
                    0
                ),
                x.get(
                    "shape_confidence",
                    0
                ),
                x.get(
                    "score",
                    0
                )
            ),
            reverse=True
        )

        return output

    def summarize(
        self,
        tables
    ):

        summary = {
            "TORQUE_PRIMARY": 0,
            "TORQUE_SECONDARY": 0,
            "TORQUE_CANDIDATE": 0,
            "UNKNOWN": 0
        }

        for table in tables:

            cls = table.get(
                "torque_classification",
                "UNKNOWN"
            )

            if cls in summary:

                summary[cls] += 1

            else:

                summary["UNKNOWN"] += 1

        return summary