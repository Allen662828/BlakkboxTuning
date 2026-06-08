# backend/core/map_correlator.py

class MapCorrelator:

    def correlate(

        self,

        axes,

        tables,

        calibration_base=0

    ):

        maps = []

        for table in tables:

            table_start = (

                calibration_base
                +
                table["address"]

            )

            table_size = (
                table["size"]
            )

            nearby_axes = []

            for axis in axes:

                axis_start = (

                    calibration_base
                    +
                    axis["address"]

                )

                distance = abs(

                    table_start
                    -
                    axis_start

                )

                if distance <= 2048:

                    nearby_axes.append({

                        "address":
                            axis_start,

                        "distance":
                            distance,

                        "span":
                            axis["span"],

                        "length":
                            axis["length"]
                    })

            nearby_axes.sort(

                key=lambda x:
                    x["distance"]
            )

            confidence = 0

            confidence += min(

                len(
                    nearby_axes
                ) * 20,

                40
            )

            confidence += min(

                table.get(
                    "smooth_ratio",
                    0
                ) * 40,

                40
            )

            confidence += min(

                table.get(
                    "unique_ratio",
                    0
                ) * 20,

                20
            )

            shape = self.detect_shape(
                table_size
            )

            maps.append({

                "table_address":
                    table_start,

                "table_size":
                    table_size,

                "shape":
                    shape,

                "axis_count":
                    len(
                        nearby_axes
                    ),

                "nearby_axes":
                    nearby_axes[:4],

                "confidence":
                    round(
                        confidence,
                        2
                    )
            })

        maps.sort(

            key=lambda x:
                x["confidence"],

            reverse=True
        )

        return maps

    def detect_shape(

        self,

        size

    ):

        lookup = {

            64: "8x8",

            100: "10x10",

            144: "12x12",

            256: "16x16",

            400: "20x20",

            512: "32x16"
        }

        return lookup.get(

            size,

            "UNKNOWN"
        )