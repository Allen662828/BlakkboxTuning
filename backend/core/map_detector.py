class MapDetector:

    AXIS_WINDOW = 16

    TABLE_SIZES = (
        64,
        128,
        256,
        400,
        512
    )

    def _score_axis(
        self,
        axis
    ):
        if len(axis) != self.AXIS_WINDOW:
            return 0.0

        if not axis:
            return 0.0

        deltas = [
            axis[i] - axis[i - 1]
            for i in range(
                1,
                len(axis)
            )
        ]

        monotonic_steps = sum(
            1
            for delta in deltas
            if delta >= 0
        )

        monotonic_ratio = (
            monotonic_steps
            /
            (
                len(axis)
                - 1
            )
        )

        span = axis[-1] - axis[0]

        if span < 20 or span > 240:
            return 0.0

        unique_ratio = (
            len(set(axis))
            /
            len(axis)
        )

        if unique_ratio < 0.60:
            return 0.0

        duplicate_count = len(axis) - len(set(axis))
        duplicate_score = max(
            0.0,
            1.0 - (duplicate_count / 6.0)
        )

        step_range = 0
        if deltas:
            step_range = max(deltas) - min(deltas)

        if not deltas:
            return 0.0

        average_step = span / (len(axis) - 1)

        if step_range <= max(4.0, average_step * 0.75):
            smoothness = 1.0
        else:
            smoothness = max(
                0.0,
                1.0 - (step_range / 96.0)
            )

        span_score = 1.0
        if span < 32:
            span_score = 0.70
        elif span < 48:
            span_score = 0.82
        elif span <= 180:
            span_score = 1.0
        else:
            span_score = 0.85

        delta_consistency = 1.0
        if average_step > 0:
            deviation = sum(
                abs(delta - average_step)
                for delta in deltas
            ) / len(deltas)

            delta_consistency = max(
                0.0,
                1.0 - (deviation / max(average_step * 2.5, 12.0))
            )

        score = (
            monotonic_ratio * 0.30
            + unique_ratio * 0.20
            + smoothness * 0.20
            + span_score * 0.15
            + delta_consistency * 0.10
            + duplicate_score * 0.05
        )

        return round(
            min(1.0, score),
            3
        )

    def _score_table(
        self,
        table
    ):
        if len(table) < 16:
            return 0.0

        minimum = min(table)
        maximum = max(table)
        span = maximum - minimum

        if span < 20 or span > 240:
            return 0.0

        deltas = [
            abs(table[i] - table[i - 1])
            for i in range(
                1,
                len(table)
            )
        ]

        if not deltas:
            return 0.0

        smooth_points = sum(
            1
            for delta in deltas
            if delta <= 15
        )

        smooth_ratio = (
            smooth_points
            /
            len(deltas)
        )

        unique_ratio = (
            len(set(table))
            /
            len(table)
        )

        mean_value = sum(table) / len(table)

        variance = sum(
            (
                x - mean_value
            ) ** 2
            for x in table
        ) / len(table)

        if variance <= 0:
            return 0.0

        variance_score = min(
            1.0,
            variance / 80.0
        )

        edge_continuity = 1.0
        edge_gap = abs(table[0] - table[-1])

        if edge_gap > 64:
            edge_continuity = max(
                0.0,
                1.0 - (edge_gap / 160.0)
            )

        jagged_ratio = sum(
            1
            for delta in deltas
            if delta > 32
        ) / len(deltas)

        jagged_score = max(
            0.0,
            1.0 - (jagged_ratio * 1.5)
        )

        span_score = 1.0
        if span < 32:
            span_score = 0.75
        elif span < 48:
            span_score = 0.85
        elif span <= 180:
            span_score = 1.0
        else:
            span_score = 0.90

        score = (
            smooth_ratio * 0.35
            + unique_ratio * 0.15
            + variance_score * 0.20
            + edge_continuity * 0.10
            + jagged_score * 0.10
            + span_score * 0.10
        )

        return round(
            min(1.0, score),
            3
        )

    def detect_axis_patterns(
        self,
        data
    ):

        axes = []

        last_axis = -999999

        length = len(data)

        for address in range(
            0,
            max(0, length - self.AXIS_WINDOW + 1)
        ):

            axis = list(
                data[
                    address:
                    address + self.AXIS_WINDOW
                ]
            )

            if len(axis) != self.AXIS_WINDOW:
                continue

            confidence = self._score_axis(axis)

            if confidence < 0.70:
                continue

            if (
                address
                -
                last_axis
            ) < self.AXIS_WINDOW:
                continue

            span = axis[-1] - axis[0]

            axes.append({

                "address":
                    address,

                "length":
                    self.AXIS_WINDOW,

                "start":
                    axis[0],

                "end":
                    axis[-1],

                "span":
                    span,

                "unique_ratio":
                    round(
                        len(set(axis)) / self.AXIS_WINDOW,
                        3
                    ),

                "confidence":
                    confidence
            })

            last_axis = address

        return axes

    def detect_table_candidates(
        self,
        data
    ):

        tables = []

        length = len(data)

        accepted_ranges = []

        for size in self.TABLE_SIZES:

            if length < size:
                continue

            for address in range(
                0,
                length - size + 1,
                16
            ):

                table = list(
                    data[
                        address:
                        address + size
                    ]
                )

                if len(table) != size:
                    continue

                confidence = self._score_table(table)

                if confidence < 0.70:
                    continue

                minimum = min(table)
                maximum = max(table)

                span = (
                    maximum
                    -
                    minimum
                )

                table_start = address
                table_end = (
                    address
                    +
                    size
                    -
                    1
                )

                overlap = False

                for rng in accepted_ranges:

                    overlap_bytes = (
                        min(
                            table_end,
                            rng[1]
                        )
                        -
                        max(
                            table_start,
                            rng[0]
                        )
                        +
                        1
                    )

                    if overlap_bytes > (
                        size * 0.75
                    ):

                        overlap = True
                        break

                if overlap:
                    continue

                accepted_ranges.append(
                    (
                        table_start,
                        table_end
                    )
                )

                mean_value = sum(table) / len(table)
                variance = sum(
                    (
                        x - mean_value
                    ) ** 2
                    for x in table
                ) / len(table)

                smooth_points = sum(
                    1
                    for i in range(
                        1,
                        len(table)
                    )
                    if abs(table[i] - table[i - 1]) <= 15
                )

                tables.append({

                    "address":
                        address,

                    "size":
                        size,

                    "min":
                        minimum,

                    "max":
                        maximum,

                    "span":
                        span,

                    "smooth_ratio":
                        round(
                            smooth_points
                            /
                            (
                                len(table)
                                - 1
                            ),
                            3
                        ),

                    "unique_ratio":
                        round(
                            len(set(table))
                            /
                            len(table),
                            3
                        ),

                    "variance":
                        round(
                            variance,
                            3
                        ),

                    "confidence":
                        confidence
                })

        return tables
