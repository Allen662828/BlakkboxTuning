class DriverDemandChain:

    def build(
        self,
        driver_wish,
        torque_limit,
        torque_monitor,
        iq_nm
    ):

        chain = []

        if driver_wish:

            chain.append(
                "DRIVER_WISH"
            )

        if torque_limit:

            chain.append(
                "TORQUE_LIMIT"
            )

        if torque_monitor:

            chain.append(
                "TORQUE_MONITOR"
            )

        if iq_nm:

            chain.append(
                "IQ_NM"
            )

        return {

            "chain":
                chain,

            "valid":
                len(chain) >= 3
        }