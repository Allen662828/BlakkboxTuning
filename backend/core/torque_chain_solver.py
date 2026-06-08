class TorqueChainSolver:

    def solve(
        self,
        driver_wish,
        torque_limiters,
        torque_monitor
    ):

        score = 0

        if driver_wish:
            score += 35

        if torque_limiters:
            score += 35

        if torque_monitor:
            score += 30

        return {

            "complete":
                score >= 80,

            "score":
                score,

            "chain": [

                "DRIVER_WISH",

                "TORQUE_LIMITER",

                "TORQUE_MONITOR"
            ]
        }