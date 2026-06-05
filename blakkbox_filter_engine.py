"""
blakkbox_filter_engine.py

BLAKKBOX Smart Delta Filter Engine

Rules

Δ0-5
    Keep 100%

Δ5-8
    Apply 80%

Δ>8
    Apply 55%

Additional:
    Remove spikes
    Preserve continuity
"""


class BlakkboxFilterEngine:

    def __init__(self):

        self.keep_limit = 5
        self.medium_limit = 8

    def filter_changes(
        self,
        changes
    ):

        filtered = []

        for change in changes:

            delta = change["delta"]

            filtered_delta = (
                self._filter_delta(
                    delta
                )
            )

            item = dict(change)

            item[
                "filtered_delta"
            ] = filtered_delta

            filtered.append(item)

        filtered = (
            self.remove_spikes(
                filtered
            )
        )

        return filtered

    def _filter_delta(
        self,
        delta
    ):

        abs_delta = abs(delta)

        #
        # Δ0-5
        #

        if abs_delta <= self.keep_limit:

            return delta

        #
        # Δ5-8
        #

        if abs_delta <= self.medium_limit:

            return round(
                delta * 0.80
            )

        #
        # Δ>8
        #

        return round(
            delta * 0.55
        )

    def remove_spikes(
        self,
        changes
    ):

        if len(changes) < 3:

            return changes

        result = list(changes)

        for i in range(
            1,
            len(changes) - 1
        ):

            prev_delta = (
                changes[i - 1]
                ["filtered_delta"]
            )

            curr_delta = (
                changes[i]
                ["filtered_delta"]
            )

            next_delta = (
                changes[i + 1]
                ["filtered_delta"]
            )

            if (
                abs(
                    curr_delta
                    -
                    prev_delta
                ) > 25
                and
                abs(
                    curr_delta
                    -
                    next_delta
                ) > 25
            ):

                result[i][
                    "filtered_delta"
                ] = round(
                    (
                        prev_delta
                        +
                        next_delta
                    ) / 2
                )

        return result

    def summarize(
        self,
        changes
    ):

        before_total = 0
        after_total = 0

        for item in changes:

            before_total += abs(
                item["delta"]
            )

            after_total += abs(
                item[
                    "filtered_delta"
                ]
            )

        reduction = 0

        if before_total > 0:

            reduction = round(
                (
                    (
                        before_total
                        -
                        after_total
                    )
                    /
                    before_total
                )
                * 100,
                2
            )

        return {

            "before_total":
                before_total,

            "after_total":
                after_total,

            "reduction_percent":
                reduction
        }