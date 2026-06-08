class DensoAirModel:

    def analyze(
        self,
        boost_maps,
        vnt_maps,
        turbo_maps
    ):

        score = 0

        if boost_maps:
            score += 40

        if vnt_maps:
            score += 30

        if turbo_maps:
            score += 30

        return {

            "air_model_score":
                score,

            "balanced":
                score >= 80
        }