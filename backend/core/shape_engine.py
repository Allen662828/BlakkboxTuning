class ShapeEngine:

    DENSO_SHAPES = {

        64: "8x8",
        100: "10x10",
        121: "11x11",
        144: "12x12",
        256: "16x16",
        320: "16x20",
        400: "20x20",
        512: "16x32",
        576: "24x24",
        1024: "32x32"
    }

    DENSO_FAMILIES = {

        "8x8": "LIMITER",
        "10x10": "DRIVER_WISH",
        "11x11": "TORQUE",
        "12x12": "RAIL_PRESSURE",
        "16x16": "TORQUE",
        "16x20": "SMOKE",
        "20x20": "BOOST",
        "16x32": "DURATION",
        "24x24": "SOI",
        "32x32": "ADVANCED"
    }

    def classify_table(
        self,
        table
    ):

        size = table.get(
            "size",
            0
        )

        if size in self.DENSO_SHAPES:

            detected_shape = (
                self.DENSO_SHAPES[size]
            )

            confidence = 100

        else:

            closest_size = min(

                self.DENSO_SHAPES.keys(),

                key=lambda x:
                abs(x - size)
            )

            detected_shape = (
                self.DENSO_SHAPES[
                    closest_size
                ]
            )

            confidence = max(

                0,

                100
                -
                abs(
                    closest_size
                    -
                    size
                )
            )

        detected_family = (

            self.DENSO_FAMILIES.get(
                detected_shape,
                "UNKNOWN"
            )

        )

        return {

            "shape":
                detected_shape,

            "family":
                detected_family,

            "confidence":
                confidence
        }

    def classify_tables(
        self,
        tables
    ):

        classified = []

        for table in tables:

            result = (
                self.classify_table(
                    table
                )
            )

            updated_table = dict(
                table
            )

            updated_table[
                "shape"
            ] = result["shape"]

            updated_table[
                "family"
            ] = result["family"]

            updated_table[
                "shape_confidence"
            ] = result["confidence"]

            classified.append(
                updated_table
            )

        return classified

    def get_family_summary(
        self,
        tables
    ):

        summary = {}

        for table in tables:

            family = table.get(
                "family",
                "UNKNOWN"
            )

            summary[family] = (

                summary.get(
                    family,
                    0
                )
                +
                1
            )

        return summary