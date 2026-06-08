class FuelAirBalanceEngine:

    def analyze(
        self,
        boost_maps,
        smoke_maps,
        rail_maps,
        duration_maps
    ):

        return {

            "boost_count":
                len(boost_maps),

            "smoke_count":
                len(smoke_maps),

            "rail_count":
                len(rail_maps),

            "duration_count":
                len(duration_maps),

            "balanced":

                min(

                    len(boost_maps),
                    len(smoke_maps),
                    len(rail_maps),
                    len(duration_maps)

                ) > 0
        }