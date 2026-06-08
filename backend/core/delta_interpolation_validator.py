class DeltaInterpolationValidator:

    def validate(
        self,
        values
    ):

        spikes = []

        for i in range(

            1,
            len(values) - 1

        ):

            prev_val = values[i - 1]
            cur_val = values[i]
            next_val = values[i + 1]

            left = abs(
                cur_val - prev_val
            )

            right = abs(
                cur_val - next_val
            )

            if (

                left > 8

                and

                right > 8

            ):

                spikes.append(i)

        return {

            "valid":
                len(spikes) == 0,

            "spike_count":
                len(spikes),

            "spikes":
                spikes
        }