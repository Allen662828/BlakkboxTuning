class AutomaticReportGenerator:

    def generate(
        self,
        analysis
    ):

        return {

            "swid":

                analysis.get(
                    "swid",
                    {}
                ),

            "detected_maps":

                analysis.get(
                    "map_ranking_summary",
                    {}
                ).get(
                    "detected_maps",
                    0
                ),

            "confidence":

                analysis.get(
                    "calibration_confidence",
                    {}
                ),

            "signature":

                analysis.get(
                    "denso_signature",
                    {}
                ),

            "oem_safe":

                analysis.get(
                    "oem_validation",
                    {}
                ),

            "status":
                "COMPLETE"
        }