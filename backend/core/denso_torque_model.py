class DensoTorqueModel:

    def analyze(
        self,
        driver_wish,
        torque_limiters,
        torque_monitor
    ):

        requested = len(
            driver_wish
        )

        limited = len(
            torque_limiters
        )

        monitored = len(
            torque_monitor
        )

        score = min(

            requested * 30 +

            limited * 40 +

            monitored * 30,

            100
        )

        return {

            "requested_maps":
                requested,

            "limiter_maps":
                limited,

            "monitor_maps":
                monitored,

            "torque_model_score":
                score,

            "valid":
                score >= 70
        }