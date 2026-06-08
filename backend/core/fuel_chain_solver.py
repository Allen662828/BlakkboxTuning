class FuelChainSolver:

    def solve(
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

            "complete":
                score >= 75,

            "score":
                score
        }