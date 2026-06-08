class OEMRegionGuard:

    def validate(
        self,
        clusters
    ):

        violations = []

        for cluster in clusters:

            classification = cluster.get(
                "classification",
                "UNKNOWN"
            )

            if classification in [

                "BOOT",
                "CHECKSUM"
            ]:

                violations.append({

                    "start":
                        cluster["start"],

                    "end":
                        cluster["end"],

                    "region":
                        classification
                })

        return {

            "safe":
                len(violations) == 0,

            "violations":
                violations
        }