class FuelRelationshipEngine:

    def build(
        self,
        smoke,
        duration,
        rail,
        iq
    ):

        return {

            "smoke":
                len(smoke),

            "duration":
                len(duration),

            "rail":
                len(rail),

            "iq":
                len(iq),

            "chain":

                [
                    "IQ",
                    "Rail",
                    "Duration",
                    "Smoke"
                ]
        }