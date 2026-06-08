class BoostRelationshipDetector:

    def build(
        self,
        boost_maps,
        torque_maps,
        smoke_maps
    ):

        relationships = []

        if boost_maps and torque_maps:

            relationships.append({

                "source":
                    "BOOST",

                "target":
                    "TORQUE",

                "relationship":
                    "AIR_SUPPLY",

                "strength":
                    95
            })

        if boost_maps and smoke_maps:

            relationships.append({

                "source":
                    "BOOST",

                "target":
                    "SMOKE_LIMITER",

                "relationship":
                    "AFR_CONTROL",

                "strength":
                    90
            })

        return relationships