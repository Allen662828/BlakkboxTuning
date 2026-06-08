# backend/core/anomaly_detector.py
#
# DENSO ROM Studio
# Calibration Surface Anomaly Detector
#
# Purpose:
# Detect:
# - Single-cell spikes
# - Surface breaks
# - Gradient discontinuities
# - Injection duration anomalies
# - Rail pressure anomalies
# - Torque map irregularities
# - Delta cluster instability
#
# Author: DENSO ROM Studio

from dataclasses import dataclass, asdict
from typing import List, Dict
import numpy as np


@dataclass
class Anomaly:

    map_name: str
    anomaly_type: str
    severity: str

    row: int
    col: int

    value: float
    expected: float

    deviation: float

    description: str


class CalibrationAnomalyDetector:

    def __init__(self):

        self.anomalies = []

    ###########################################################################
    # SINGLE CELL SPIKE DETECTOR
    ###########################################################################

    def detect_spikes(
        self,
        map_data,
        map_name,
        threshold=20.0
    ):

        rows, cols = map_data.shape

        for r in range(rows):

            for c in range(1, cols - 1):

                left = map_data[r][c - 1]
                center = map_data[r][c]
                right = map_data[r][c + 1]

                expected = (left + right) / 2.0

                deviation = abs(center - expected)

                if deviation > threshold:

                    severity = (
                        "critical"
                        if deviation > threshold * 3
                        else "warning"
                    )

                    self.anomalies.append(

                        Anomaly(
                            map_name=map_name,
                            anomaly_type="single_cell_spike",
                            severity=severity,
                            row=r,
                            col=c,
                            value=float(center),
                            expected=float(expected),
                            deviation=float(deviation),
                            description=(
                                f"Cell differs from neighbors "
                                f"by {deviation:.2f}"
                            )
                        )
                    )

    ###########################################################################
    # GRADIENT BREAK DETECTOR
    ###########################################################################

    def detect_gradient_breaks(
        self,
        map_data,
        map_name,
        threshold=25.0
    ):

        rows, cols = map_data.shape

        for r in range(rows):

            row = map_data[r]

            first_derivative = np.diff(row)

            second_derivative = np.diff(first_derivative)

            for i, val in enumerate(second_derivative):

                if abs(val) > threshold:

                    self.anomalies.append(

                        Anomaly(
                            map_name=map_name,
                            anomaly_type="gradient_break",
                            severity="warning",
                            row=r,
                            col=i + 1,
                            value=float(row[i + 1]),
                            expected=float(row[i]),
                            deviation=float(abs(val)),
                            description=(
                                "Second derivative exceeds threshold"
                            )
                        )
                    )

    ###########################################################################
    # SURFACE CONTINUITY
    ###########################################################################

    def calculate_surface_score(
        self,
        map_data
    ):

        variances = []

        rows, cols = map_data.shape

        for r in range(rows - 2):

            for c in range(cols - 2):

                block = map_data[r:r + 3, c:c + 3]

                variances.append(np.var(block))

        if not variances:
            return 100.0

        avg_var = np.mean(variances)

        score = max(0.0, 100.0 - avg_var)

        return round(score, 2)

    ###########################################################################
    # INJECTION DURATION VALIDATOR
    ###########################################################################

    def validate_injection_duration(
        self,
        map_data,
        map_name="main_injection_time",
        threshold_percent=20.0
    ):

        rows, cols = map_data.shape

        for r in range(1, rows - 1):

            for c in range(1, cols - 1):

                neighborhood = map_data[
                    r - 1:r + 2,
                    c - 1:c + 2
                ]

                center = map_data[r][c]

                neighbors = np.delete(
                    neighborhood.flatten(),
                    4
                )

                expected = np.mean(neighbors)

                if expected == 0:
                    continue

                deviation_pct = (
                    abs(center - expected)
                    / expected
                    * 100.0
                )

                if deviation_pct > threshold_percent:

                    severity = (
                        "critical"
                        if deviation_pct > 40
                        else "warning"
                    )

                    self.anomalies.append(

                        Anomaly(
                            map_name=map_name,
                            anomaly_type="duration_surface_break",
                            severity=severity,
                            row=r,
                            col=c,
                            value=float(center),
                            expected=float(expected),
                            deviation=float(deviation_pct),
                            description=(
                                f"Injection duration differs "
                                f"{deviation_pct:.1f}% "
                                f"from neighborhood"
                            )
                        )
                    )

    ###########################################################################
    # RAIL PRESSURE VALIDATOR
    ###########################################################################

    def validate_rail_pressure(
        self,
        map_data,
        threshold_percent=15.0
    ):

        rows, cols = map_data.shape

        for r in range(rows):

            for c in range(1, cols):

                previous = map_data[r][c - 1]
                current = map_data[r][c]

                if previous == 0:
                    continue

                delta_pct = (
                    abs(current - previous)
                    / previous
                    * 100.0
                )

                if delta_pct > threshold_percent:

                    self.anomalies.append(

                        Anomaly(
                            map_name="rail_pressure",
                            anomaly_type="rail_jump",
                            severity="warning",
                            row=r,
                            col=c,
                            value=float(current),
                            expected=float(previous),
                            deviation=float(delta_pct),
                            description=(
                                f"Rail pressure jump "
                                f"{delta_pct:.1f}%"
                            )
                        )
                    )

    ###########################################################################
    # DELTA ANALYSIS
    ###########################################################################

    def analyze_delta_map(
        self,
        delta_map
    ):

        delta_map = np.abs(delta_map)

        return {

            "modified_cells":
                int(np.count_nonzero(delta_map)),

            "mean_delta":
                float(np.mean(delta_map)),

            "max_delta":
                float(np.max(delta_map)),

            "std_delta":
                float(np.std(delta_map))
        }

    ###########################################################################
    # BLAKKBOX QUALITY SCORE
    ###########################################################################

    def calculate_quality_score(
        self,
        continuity_score,
        interpolation_score,
        torque_chain_score,
        delta_score
    ):

        quality = (

            continuity_score * 0.30 +
            interpolation_score * 0.30 +
            torque_chain_score * 0.20 +
            delta_score * 0.20
        )

        return round(quality, 2)

    ###########################################################################
    # EXPORT
    ###########################################################################

    def export_results(self):

        return {

            "anomaly_count":
                len(self.anomalies),

            "anomalies":
                [asdict(a) for a in self.anomalies]
        }


###############################################################################
# EXAMPLE
###############################################################################

if __name__ == "__main__":

    detector = CalibrationAnomalyDetector()

    example = np.array([

        [535, 491, 480],
        [535, 212, 491],
        [520, 505, 495]

    ])

    detector.detect_spikes(
        example,
        "main_injection_time"
    )

    detector.validate_injection_duration(
        example
    )

    print(detector.export_results())