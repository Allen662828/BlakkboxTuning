class TorqueHierarchyValidator:

    def validate(
        self,
        driver_wish,
        torque_limiters,
        torque_monitor
    ):

        report = {

            "valid": True,

            "issues": []
        }

        if len(driver_wish) == 0:

            report["valid"] = False

            report["issues"].append(
                "NO_DRIVER_WISH"
            )

        if len(torque_limiters) == 0:

            report["valid"] = False

            report["issues"].append(
                "NO_TORQUE_LIMITER"
            )

        if len(torque_monitor) == 0:

            report["valid"] = False

            report["issues"].append(
                "NO_TORQUE_MONITOR"
            )

        if (

            len(driver_wish)
            >

            len(torque_limiters)

        ):

            report["issues"].append(

                "DRIVER_WISH_EXCEEDS_LIMITERS"
            )

        return report