class DensoFuelModel:

    def analyze(
        self,
        smoke_maps,
        duration_maps,
        rail_maps,
        iq_maps
    ):

        score = 0

        score += min(
            len(smoke_maps) * 25,
            25
        )

        score += min(
            len(duration_maps) * 25,
            25
        )

        score += min(
            len(rail_maps) * 25,
            25
        )

        score += min(
            len(iq_maps) * 25,
            25
        )

        return {

            "fuel_model_score":
                score,

            "balanced":
                score >= 75
        }