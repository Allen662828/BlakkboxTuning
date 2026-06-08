class MapNamingEngine:

    def __init__(self):

        self.family_names = {

            "DRIVER_WISH":
                "Driver Wish",

            "TORQUE_LIMITER":
                "Torque Limiter",

            "TORQUE_MONITOR":
                "Torque Monitor",

            "BOOST_TARGET":
                "Boost Target",

            "VNT":
                "VNT Control",

            "SMOKE_LIMITER":
                "Smoke Limiter",

            "RAIL_PRESSURE":
                "Rail Pressure",

            "DURATION":
                "Injection Duration",

            "SOI":
                "Start Of Injection",

            "IQ_NM":
                "IQ To Torque"
        }

    def classify(
        self,
        tables
    ):

        output = []

        for table in tables:

            family = table.get(
                "family",
                "UNKNOWN"
            )

            output.append({

                "address":
                    table.get(
                        "absolute_start",
                        0
                    ),

                "family":
                    family,

                "name":
                    self.family_names.get(
                        family,
                        family
                    ),

                "confidence":
                    table.get(
                        "shape_confidence",
                        0
                    )
            })

        return output