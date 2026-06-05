"""
delta_analyzer.py

BLAKKBOX Delta Severity Analyzer
"""


class DeltaAnalyzer:

    def __init__(self):

        self.low_limit = 5
        self.medium_limit = 8

    def analyze(
        self,
        changes
    ):

        band_0_5 = 0
        band_5_8 = 0
        band_8_plus = 0

        total_changed = len(changes)

        if total_changed == 0:

            return {

                "severity": "OEM",

                "risk_level": "NONE",

                "risk_score": 0,

                "total_changed": 0,

                "0_5": {
                    "count": 0,
                    "percent": 0
                },

                "5_8": {
                    "count": 0,
                    "percent": 0
                },

                "8_plus": {
                    "count": 0,
                    "percent": 0
                }
            }

        for change in changes:

            delta = abs(
                change["delta"]
            )

            if delta <= self.low_limit:

                band_0_5 += 1

            elif delta <= self.medium_limit:

                band_5_8 += 1

            else:

                band_8_plus += 1

        pct_0_5 = round(
            (
                band_0_5 /
                total_changed
            ) * 100,
            2
        )

        pct_5_8 = round(
            (
                band_5_8 /
                total_changed
            ) * 100,
            2
        )

        pct_8_plus = round(
            (
                band_8_plus /
                total_changed
            ) * 100,
            2
        )

        severity = (
            self.determine_severity(
                pct_8_plus
            )
        )

        risk_level = (
            self.determine_risk(
                pct_8_plus
            )
        )

        return {

            "severity":
                severity,

            "risk_level":
                risk_level,

            "risk_score":
                pct_8_plus,

            "total_changed":
                total_changed,

            "0_5": {

                "count":
                    band_0_5,

                "percent":
                    pct_0_5
            },

            "5_8": {

                "count":
                    band_5_8,

                "percent":
                    pct_5_8
            },

            "8_plus": {

                "count":
                    band_8_plus,

                "percent":
                    pct_8_plus
            }
        }

    def determine_severity(
        self,
        pct_8_plus
    ):

        if pct_8_plus < 15:
            return "OEM_PLUS"

        if pct_8_plus < 30:
            return "SPORTS"

        if pct_8_plus < 50:
            return "AGGRESSIVE"

        return "OVER_MODIFIED"

    def determine_risk(
        self,
        pct_8_plus
    ):

        if pct_8_plus < 15:
            return "LOW"

        if pct_8_plus < 30:
            return "MEDIUM"

        if pct_8_plus < 50:
            return "HIGH"

        return "EXTREME"