class TorqueRelationshipEngine:

    def build(
        self,
        driver_wish,
        torque_limiters,
        torque_monitors
    ):

        return {

            "driver_wish":
                len(
                    driver_wish
                ),

            "torque_limiters":
                len(
                    torque_limiters
                ),

            "torque_monitors":
                len(
                    torque_monitors
                ),

            "chain":

                [
                    "Driver Wish",
                    "Torque Limiter",
                    "Torque Monitor"
                ]
        }