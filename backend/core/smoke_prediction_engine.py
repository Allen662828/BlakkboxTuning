class SmokePredictionEngine:

    def predict(
        self,
        boost_kpa,
        fuel_mg
    ):

        afr = 0

        if fuel_mg > 0:

            afr = round(

                boost_kpa
                / fuel_mg,

                2
            )

        if afr >= 3.0:

            level = "LOW"

        elif afr >= 2.2:

            level = "MEDIUM"

        else:

            level = "HIGH"

        return {

            "afr_ratio":
                afr,

            "smoke_level":
                level
        }