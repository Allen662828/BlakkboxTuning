class MapFamilyClassifier:

    def classify(
        self,
        tables
    ):

        families = {}

        for table in tables:

            family = table.get(
                "family",
                "UNKNOWN"
            )

            families[family] = (

                families.get(
                    family,
                    0
                )

                + 1
            )

        return families