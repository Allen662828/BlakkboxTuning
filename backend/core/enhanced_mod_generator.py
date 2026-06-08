from .blakkbox_delta_filter import (
    BlakkboxDeltaFilter
)

from .smart_delta_optimizer import (
    SmartDeltaOptimizer
)

from .mod_rebuilder import (
    ModRebuilder
)


class EnhancedModGenerator:

    def __init__(self):

        self.filter = (
            BlakkboxDeltaFilter()
        )

        self.optimizer = (
            SmartDeltaOptimizer()
        )

        self.rebuilder = (
            ModRebuilder()
        )

    def _remove_spikes(
        self,
        changes
    ):

        cleaned = []

        for change in changes:

            delta = abs(
                change.get(
                    "filtered_delta",
                    0
                )
            )

            if delta > 40:

                change = dict(change)

                change[
                    "filtered_delta"
                ] = round(
                    change[
                        "filtered_delta"
                    ] * 0.75
                )

            cleaned.append(change)

        return cleaned

    def generate(
        self,
        original,
        changes,
        context=None
    ):

        optimized = (
            self.optimizer.optimize(
                changes
            )
        )

        filtered = (
            self.filter.filter_delta(
                optimized,
                context=context
            )
        )

        filtered = (
            self._remove_spikes(
                filtered
            )
        )

        return (
            self.rebuilder.rebuild(
                original,
                filtered
            )
        )