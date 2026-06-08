class AutomaticMapClassifier:

    def classify(
        self,
        tables
    ):

        classified = []

        for table in tables:

            family = table.get(
                "family",
                "UNKNOWN"
            )

            confidence = table.get(
                "confidence",
                0
            )

            if confidence >= 90:

                level = "HIGH"

            elif confidence >= 75:

                level = "MEDIUM"

            else:

                level = "LOW"

            table["classification"] = {

                "family":
                    family,

                "level":
                    level
            }

            classified.append(
                table
            )

        return classified