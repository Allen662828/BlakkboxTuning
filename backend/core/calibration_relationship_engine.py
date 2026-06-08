class CalibrationRelationshipEngine:

    def build(
        self,
        driver_wish_maps,
        torque_maps,
        iq_maps,
        limiter_maps,
        smoke_maps,
        duration_maps,
        rail_maps,
        boost_maps,
        soi_maps
    ):

        relationships = []

        if driver_wish_maps and torque_maps:

            relationships.append({

                "source":
                    "DRIVER_WISH",

                "target":
                    "TORQUE_LIMITER",

                "strength":
                    100
            })

        if torque_maps and iq_maps:

            relationships.append({

                "source":
                    "TORQUE_LIMITER",

                "target":
                    "IQ_NM",

                "strength":
                    95
            })

        if iq_maps and smoke_maps:

            relationships.append({

                "source":
                    "IQ_NM",

                "target":
                    "SMOKE_LIMITER",

                "strength":
                    90
            })

        if smoke_maps and duration_maps:

            relationships.append({

                "source":
                    "SMOKE_LIMITER",

                "target":
                    "DURATION",

                "strength":
                    90
            })

        if duration_maps and rail_maps:

            relationships.append({

                "source":
                    "DURATION",

                "target":
                    "RAIL_PRESSURE",

                "strength":
                    85
            })

        if boost_maps and torque_maps:

            relationships.append({

                "source":
                    "BOOST",

                "target":
                    "TORQUE",

                "strength":
                    85
            })

        if soi_maps and duration_maps:

            relationships.append({

                "source":
                    "SOI",

                "target":
                    "DURATION",

                "strength":
                    80
            })

        return relationships