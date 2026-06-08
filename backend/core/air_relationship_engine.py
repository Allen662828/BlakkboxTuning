class AirRelationshipEngine:

    def build(
        self,
        boost,
        vnt,
        protection
    ):

        return {

            "boost":
                len(boost),

            "vnt":
                len(vnt),

            "protection":
                len(protection),

            "chain":

                [
                    "Boost",
                    "VNT",
                    "Protection"
                ]
        }