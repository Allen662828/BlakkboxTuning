class TorqueChainValidator:

    def validate(
        self,
        driver_wish,
        torque,
        iq,
        limiter
    ):

        issues = []

        if not driver_wish:

            issues.append(
                "Missing Driver Wish"
            )

        if not torque:

            issues.append(
                "Missing Torque Limiter"
            )

        if not iq:

            issues.append(
                "Missing IQ Conversion"
            )

        if not limiter:

            issues.append(
                "Missing Limiter Stack"
            )

        return {

            "valid":
                len(issues) == 0,

            "issues":
                issues
        }