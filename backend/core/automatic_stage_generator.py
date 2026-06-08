class AutomaticStageGenerator:

    def generate(
        self,
        classified_maps
    ):

        recommendations = []

        for table in classified_maps:

            family = table.get(
                "family",
                ""
            )

            if family in [

                "DRIVER_WISH",
                "TORQUE_LIMITER"

            ]:

                recommendations.append({

                    "map":
                        table.get(
                            "name"
                        ),

                    "delta":
                        "+8%"
                })

            elif family in [

                "BOOST",
                "VNT"

            ]:

                recommendations.append({

                    "map":
                        table.get(
                            "name"
                        ),

                    "delta":
                        "+5%"
                })

        return {

            "stage":
                "STAGE_1",

            "recommendations":
                recommendations
        }