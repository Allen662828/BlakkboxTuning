class RailRelationshipDetector:

    def build(
        self,
        rail_maps,
        duration_maps,
        iq_maps
    ):

        relationships = []

        if rail_maps and duration_maps:

            relationships.append({

                "source":
                    "RAIL_PRESSURE",

                "target":
                    "DURATION",

                "relationship":
                    "INJECTION_FLOW",

                "strength":
                    95
            })

        if rail_maps and iq_maps:

            relationships.append({

                "source":
                    "RAIL_PRESSURE",

                "target":
                    "IQ",

                "relationship":
                    "FUEL_DELIVERY",

                "strength":
                    90
            })

        return relationships