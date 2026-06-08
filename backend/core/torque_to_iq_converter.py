class TorqueToIQConverter:

    def convert(
        self,
        torque_nm
    ):

        iq = round(

            torque_nm
            / 8.5,

            2
        )

        return {

            "torque_nm":
                torque_nm,

            "iq_mg":
                iq
        }

    def batch_convert(
        self,
        torque_values
    ):

        return [

            self.convert(v)

            for v

            in torque_values
        ]