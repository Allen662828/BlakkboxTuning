class AirChainSolver:

    def solve(
        self,
        boost_maps,
        vnt_maps,
        turbo_protection_maps
    ):

        score = 0

        if boost_maps:
            score += 40

        if vnt_maps:
            score += 30

        if turbo_protection_maps:
            score += 30

        return {

            "complete":
                score >= 80,

            "score":
                score
        }