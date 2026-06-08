import json


class CalibrationExportEngine:

    def export_json(
        self,
        report,
        filename
    ):

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as handle:

            json.dump(

                report,

                handle,

                indent=4
            )

    def export_summary(
        self,
        report
    ):

        return {

            "swid":

                report.get(
                    "swid",
                    {}
                ),

            "detected_maps":

                report.get(
                    "map_ranking_summary",
                    {}
                ).get(
                    "detected_maps",
                    0
                ),

            "clusters":

                report.get(
                    "processor_analysis",
                    {}
                ).get(
                    "cluster_count",
                    0
                )
        }