"""
bin_comparator.py

DENSO ROM Comparator
"""


class BinComparator:

    def __init__(
        self,
        original,
        modified
    ):

        self.original = original
        self.modified = modified

        if len(original) != len(modified):

            raise ValueError(
                "BIN size mismatch"
            )

    def compare_bytes(self):

        changes = []

        for addr, (o, m) in enumerate(
            zip(
                self.original,
                self.modified
            )
        ):

            if o != m:

                changes.append({

                    "address":
                        addr,

                    "address_hex":
                        hex(addr),

                    "original":
                        o,

                    "modified":
                        m,

                    "delta":
                        m - o
                })

        return changes

    def find_modified_regions(self):

        regions = []

        start = None

        for i in range(
            len(self.original)
        ):

            if (
                self.original[i]
                !=
                self.modified[i]
            ):

                if start is None:

                    start = i

            else:

                if start is not None:

                    regions.append({

                        "start":
                            start,

                        "end":
                            i - 1,

                        "length":
                            i - start
                    })

                    start = None

        if start is not None:

            regions.append({

                "start":
                    start,

                "end":
                    len(self.original) - 1,

                "length":
                    len(self.original) - start
            })

        return regions

    def cluster_changes(
        self,
        merge_distance=32
    ):

        regions = (
            self.find_modified_regions()
        )

        if not regions:

            return []

        clusters = []

        current = dict(
            regions[0]
        )

        for region in regions[1:]:

            gap = (
                region["start"]
                -
                current["end"]
            )

            if gap <= merge_distance:

                current["end"] = (
                    region["end"]
                )

                current["length"] = (

                    current["end"]
                    -
                    current["start"]
                    +
                    1
                )

            else:

                clusters.append(
                    current
                )

                current = dict(
                    region
                )

        clusters.append(
            current
        )

        return clusters

    def calculate_delta_stats(self):

        changed_bytes = 0

        positive_changes = 0

        negative_changes = 0

        max_delta = 0

        total_abs_delta = 0

        for o, m in zip(
            self.original,
            self.modified
        ):

            if o != m:

                changed_bytes += 1

                delta = (
                    m - o
                )

                total_abs_delta += (
                    abs(delta)
                )

                if delta > 0:

                    positive_changes += 1

                elif delta < 0:

                    negative_changes += 1

                if (
                    abs(delta)
                    >
                    max_delta
                ):

                    max_delta = (
                        abs(delta)
                    )

        avg_delta = 0

        if changed_bytes:

            avg_delta = round(

                total_abs_delta
                /
                changed_bytes,

                2
            )

        return {

            "changed_bytes":
                changed_bytes,

            "positive_changes":
                positive_changes,

            "negative_changes":
                negative_changes,

            "max_delta":
                max_delta,

            "average_delta":
                avg_delta
        }

    def get_change_density(self):

        changed = 0

        total = len(
            self.original
        )

        for o, m in zip(
            self.original,
            self.modified
        ):

            if o != m:

                changed += 1

        density = 0

        if total:

            density = round(

                (
                    changed
                    /
                    total
                ) * 100,

                4
            )

        return {

            "changed":
                changed,

            "total":
                total,

            "density_percent":
                density
        }
