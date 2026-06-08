class SmartDeltaOptimizer:

    def _cluster_changes(self, changes):

        if not changes:
            return []

        changes = sorted(
            changes,
            key=lambda x: x["address"]
        )

        clusters = []
        current = [changes[0]]

        for change in changes[1:]:

            if (
                change["address"]
                -
                current[-1]["address"]
                <= 16
            ):
                current.append(change)

            else:
                clusters.append(current)
                current = [change]

        clusters.append(current)

        return clusters

    def _smooth_cluster(self, cluster):

        if len(cluster) < 3:
            return cluster

        output = []

        for i, change in enumerate(cluster):

            delta = float(change["delta"])

            if i > 0 and i < len(cluster) - 1:

                prev_delta = float(
                    cluster[i - 1]["delta"]
                )

                next_delta = float(
                    cluster[i + 1]["delta"]
                )

                avg = (
                    prev_delta
                    +
                    delta
                    +
                    next_delta
                ) / 3

                if abs(delta - avg) > 8:
                    delta = avg

            item = dict(change)
            item["delta"] = round(delta, 2)

            output.append(item)

        return output

    def optimize(self, changes):

        clusters = self._cluster_changes(
            changes
        )

        optimized = []

        for cluster in clusters:

            cluster = self._smooth_cluster(
                cluster
            )

            for change in cluster:

                delta = float(
                    change["delta"]
                )

                if abs(delta) <= 5:
                    new_delta = delta

                elif abs(delta) <= 8:
                    new_delta = delta * 0.80

                else:
                    new_delta = delta * 0.55

                item = dict(change)

                item["delta"] = round(
                    new_delta,
                    2
                )

                optimized.append(item)

        return optimized