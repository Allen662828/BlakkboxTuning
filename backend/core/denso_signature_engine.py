class DensoSignatureEngine:

    def detect(
        self,
        swid,
        maps
    ):

        family = swid.get(
            "family",
            "UNKNOWN"
        )

        score = 0

        if family != "UNKNOWN":

            score += 50

        if len(maps) > 25:

            score += 25

        if len(maps) > 50:

            score += 25

        score = min(
            score,
            100
        )

        return {

            "family":
                family,

            "signature_score":
                score,

            "detected_maps":
                len(maps),

            "platform":
                "DENSO"
        }