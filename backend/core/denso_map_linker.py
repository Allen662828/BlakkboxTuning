class DensoMapLinker:

    def __init__(self):

        pass

    def _find_axes(
        self,
        table,
        axes
    ):

        table_start = table.get(
            "address",
            0
        )

        x_axis = None
        y_axis = None

        candidates = []

        for axis in axes:

            axis_start = axis.get(
                "address",
                0
            )

            axis_length = axis.get(
                "length",
                0
            )

            axis_end = (
                axis_start
                +
                axis_length
            )

            if axis_end >= table_start:

                continue

            distance = (
                table_start
                -
                axis_end
            )

            if distance > self.max_axis_gap:

                continue

            candidates.append({

                "axis":
                    axis,

                "distance":
                    distance
            })

        candidates = sorted(

            candidates,

            key=lambda x:
                x["distance"]
        )

        if len(candidates) >= 1:

            x_axis = (
                candidates[0]["axis"]
            )

        if len(candidates) >= 2:

            y_axis = (
                candidates[1]["axis"]
            )

        return (
            x_axis,
            y_axis
        )

    def link(
        self,
        maps,
        axes
    ):

        linked = []

        for table in maps:

            x_axis, y_axis = (

                self._find_axes(
                    table,
                    axes
                )

            )

            confidence = 0

            if x_axis:

                confidence += 50

            if y_axis:

                confidence += 30

            if table.get(
                "shape_confidence",
                0
            ) >= 80:

                confidence += 20

            linked.append({

                "table":
                    table,

                "x_axis":
                    x_axis,

                "y_axis":
                    y_axis,

                "linked":

                    (
                        x_axis
                        is not None
                    ),

                "confidence":
                    confidence
            })

        return sorted(

            linked,

            key=lambda x:
                x["confidence"],

            reverse=True
        )

    def summary(
        self,
        linked_maps
    ):

        linked_count = sum(

            1

            for item

            in linked_maps

            if item.get(
                "linked",
                False
            )
        )

        return {

            "total_maps":
                len(
                    linked_maps
                ),

            "linked_maps":
                linked_count,

            "unlinked_maps":

                len(
                    linked_maps
                )

                -

                linked_count
        }