class BlakkboxDeltaFilter:

    def __init__(self):

        self.low_threshold = 5
        self.mid_threshold = 8

    def _classification_bias(self, classification):

        classification = str(classification or "UNKNOWN").upper()

        if classification in {"BOOT", "CODE", "CHECKSUM"}:
            return 0.0

        if classification == "CALIBRATION":
            return 1.0

        if classification == "UNKNOWN":
            return 0.95

        return 0.90

    def _family_bias(self, family):

        family = str(family or "UNKNOWN").upper()

        if family in {"TORQUE", "DRIVER_WISH", "LIMITER", "IQ_NM"}:
            return 0.97

        if family in {"BOOST", "AIR", "VNT", "TURBO"}:
            return 0.94

        if family in {"RAIL", "FUEL"}:
            return 0.90

        if family in {"SMOKE", "DURATION", "SOI", "DTC"}:
            return 0.88

        return 1.0

    def _confidence_bias(self, confidence):

        if confidence is None:
            return 1.0

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            return 1.0

        if confidence < 60:
            return 0.85

        if confidence < 80:
            return 0.95

        return 1.0

    def _stability_bias(self, change, context):

        neighbor_deltas = []

        if isinstance(context, dict):
            neighbor_deltas = context.get("neighbor_deltas") or []

        if not neighbor_deltas:
            return 1.0

        values = []

        for item in neighbor_deltas:

            try:
                values.append(abs(float(item)))
            except (TypeError, ValueError):
                continue

        if not values:
            return 1.0

        values.sort()

        reference = values[len(values) // 2]

        try:
            current = abs(float(change.get("delta", 0)))
        except (TypeError, ValueError):
            return 1.0

        if reference <= 0:
            return 1.0

        if current > reference * 2.5:
            return 0.75

        if current > reference * 1.6:
            return 0.90

        return 1.0

    def filter_delta(
        self,
        changes,
        context=None
    ):

        context = context or {}
        filtered = []

        for change in changes:

            delta = change.get("delta", 0)

            try:
                delta = float(delta)
            except (TypeError, ValueError):
                delta = 0.0

            classification = change.get(
                "classification",
                context.get("classification")
            )

            family = change.get(
                "family",
                change.get("map_family", context.get("family"))
            )

            if abs(delta) <= self.low_threshold:
                filtered_delta = delta
            elif abs(delta) <= self.mid_threshold:
                filtered_delta = delta * 0.80
            else:
                filtered_delta = delta * 0.55

            filtered_delta *= self._classification_bias(classification)
            filtered_delta *= self._family_bias(family)
            filtered_delta *= self._confidence_bias(
                change.get("confidence", context.get("confidence"))
            )
            filtered_delta *= self._stability_bias(change, context)

            if change.get("is_spike") or change.get("outlier"):
                filtered_delta *= 0.70

            output = dict(change)

            output["filtered_delta"] = round(filtered_delta)
            output["filter_profile"] = {
                "classification": str(classification or "UNKNOWN").upper(),
                "family": str(family or "UNKNOWN").upper(),
                "source_delta": delta,
            }

            filtered.append(output)

        return filtered
