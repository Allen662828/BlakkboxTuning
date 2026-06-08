class EGRDetector:

    def detect(
        self,
        tables
    ):

        output = []

        for table in tables:

            size = table.get(
                "size",
                0
            )

            family = table.get(
                "family",
                ""
            )

            if size < 64:
                continue

            if family in (

                "SMOKE_LIMITER",
                "BOOST_TARGET",
                "RAIL_PRESSURE"

            ):
                continue

            output.append({

                "address":
                    table.get(
                        "absolute_start",
                        0
                    ),

                "size":
                    size,

                "suspected_egr":
                    True,

                "confidence":
                    60
            })

        return output