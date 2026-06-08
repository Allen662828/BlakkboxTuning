class OEMStructureGuard:

    def __init__(self):

        self.protected_regions = {

            "BOOT",
            "CODE",
            "CHECKSUM"
        }

    def validate(
        self,
        clusters
    ):

        violations = []

        for cluster in clusters:

            classification = (

                cluster.get(
                    "classification",
                    "UNKNOWN"
                )

            )

            if (

                classification

                in

                self.protected_regions

            ):

                violations.append({

                    "start":

                        cluster.get(
                            "start",
                            0
                        ),

                    "end":

                        cluster.get(
                            "end",
                            0
                        ),

                    "length":

                        cluster.get(
                            "length",
                            0
                        ),

                    "region":
                        classification
                })

        return {

            "safe":

                len(
                    violations
                ) == 0,

            "violation_count":

                len(
                    violations
                ),

            "violations":
                violations
        }

    def validate_calibration_only(
        self,
        clusters
    ):

        result = (
            self.validate(
                clusters
            )
        )

        return result[
            "safe"
        ]