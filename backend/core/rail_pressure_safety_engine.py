class RailPressureSafetyEngine:

    def analyze(
        self,
        rail_values
    ):

        max_rail = max(
            rail_values,
            default=0
        )

        warnings = []

        if max_rail > 185000:

            warnings.append(
                "HIGH_RAIL_PRESSURE"
            )

        if max_rail > 195000:

            warnings.append(
                "CRITICAL_RAIL_PRESSURE"
            )

        return {

            "max_rail":
                max_rail,

            "safe":
                max_rail <= 185000,

            "warnings":
                warnings
        }