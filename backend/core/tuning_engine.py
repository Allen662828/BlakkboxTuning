from .bin_comparator import BinComparator
from .region_classifier import RegionClassifier
from .delta_analyzer import DeltaAnalyzer
from .oem_validator import OEMValidator
from .map_detector import MapDetector
from .swid_detector import SWIDDetector
from .region_density import RegionDensity
from .map_ranker import MapRanker
from .map_correlator import MapCorrelator
from .shape_engine import ShapeEngine
from .torque_structure_detector import TorqueStructureDetector
from .boost_structure_detector import BoostStructureDetector
from .rail_pressure_detector import RailPressureDetector
from .smoke_limiter_detector import SmokeLimiterDetector
from .duration_detector import DurationDetector
from .soi_detector import SOIDetector
from .driver_wish_detector import DriverWishDetector
from .iq_nm_detector import IQNmDetector
from .limiter_stack_detector import LimiterStackDetector
from .calibration_relationship_engine import CalibrationRelationshipEngine
from .calibration_confidence import CalibrationConfidence
from .denso_signature_engine import DensoSignatureEngine
from .map_naming_engine import MapNamingEngine
from .egr_detector import EGRDetector
from .dtc_detector import DTCDetector
from .torque_relationship_engine import TorqueRelationshipEngine
from .fuel_relationship_engine import FuelRelationshipEngine
from .air_relationship_engine import AirRelationshipEngine
from .calibration_export_engine import CalibrationExportEngine
from .denso_torque_model import DensoTorqueModel
from .denso_fuel_model import DensoFuelModel
from .denso_air_model import DensoAirModel
from .map_similarity_engine import MapSimilarityEngine
from .delta_interpolation_validator import DeltaInterpolationValidator
from .torque_to_iq_converter import TorqueToIQConverter
from .rail_pressure_safety_engine import RailPressureSafetyEngine
from .smoke_prediction_engine import SmokePredictionEngine
from .anomaly_detector import CalibrationAnomalyDetector

import numpy as np


class BlakkboxTuningEngine:

    def __init__(self):

        self.delta_analyzer = DeltaAnalyzer()
        self.oem_validator = OEMValidator()
        self.map_detector = MapDetector()
        self.swid_detector = SWIDDetector()
        self.region_density = RegionDensity()

        self.map_ranker = MapRanker()
        self.map_correlator = MapCorrelator()
        self.shape_engine = ShapeEngine()

        self.torque_structure_detector = TorqueStructureDetector()
        self.boost_detector = BoostStructureDetector()
        self.rail_detector = RailPressureDetector()
        self.smoke_detector = SmokeLimiterDetector()

        self.duration_detector = DurationDetector()
        self.soi_detector = SOIDetector()
        self.driver_wish_detector = DriverWishDetector()
        self.iq_nm_detector = IQNmDetector()
        self.limiter_stack_detector = LimiterStackDetector()

        self.relationship_engine = CalibrationRelationshipEngine()
        self.confidence_engine = CalibrationConfidence()
        self.signature_engine = DensoSignatureEngine()

        self.map_naming_engine = MapNamingEngine()
        self.egr_detector = EGRDetector()
        self.dtc_detector = DTCDetector()

        self.torque_relationship_engine = TorqueRelationshipEngine()
        self.fuel_relationship_engine = FuelRelationshipEngine()
        self.air_relationship_engine = AirRelationshipEngine()

        self.export_engine = CalibrationExportEngine()

        self.torque_model = DensoTorqueModel()
        self.fuel_model = DensoFuelModel()
        self.air_model = DensoAirModel()

        self.similarity_engine = MapSimilarityEngine()
        self.interpolation_validator = DeltaInterpolationValidator()
        self.torque_to_iq = TorqueToIQConverter()
        self.rail_safety = RailPressureSafetyEngine()
        self.smoke_predictor = SmokePredictionEngine()

        self.anomaly_detector = CalibrationAnomalyDetector()

    def _build_matrix(self, table, calibration_data):
        address = table.get("address", 0)
        size = table.get("size", 0)

        raw = calibration_data[address:address + size]

        shapes = {
            64: (8, 8),
            100: (10, 10),
            121: (11, 11),
            144: (12, 12),
            256: (16, 16),
            320: (16, 20),
            400: (20, 20),
            512: (16, 32),
        }

        if size not in shapes:
            return None

        rows, cols = shapes[size]

        try:
            arr = np.array(raw, dtype=float)
            if arr.size != rows * cols:
                return None
            return arr.reshape(rows, cols)
        except Exception:
            return None

    def analyze(
        self,
        original,
        modified,
        filename=""
    ):

        filesize = len(original)

        self.anomaly_detector.anomalies = []

        swid = self.swid_detector.detect(filename)

        comparator = BinComparator(
            original,
            modified
        )

        changes = comparator.compare_bytes()
        modified_regions = comparator.find_modified_regions()
        clusters = comparator.cluster_changes()
        delta_stats = comparator.calculate_delta_stats()

        classifier = RegionClassifier(
            filesize,
            swid["family"]
        )

        modified_regions = classifier.classify_regions(
            modified_regions
        )

        clusters = classifier.classify_regions(
            clusters
        )

        density = self.region_density.analyze(
            clusters
        )

        delta_analysis = self.delta_analyzer.analyze(
            changes
        )

        oem_validation = self.oem_validator.validate(
            original,
            modified,
            modified_regions
        )

        layout = classifier.get_layout()

        cal_start = layout["calibration"][0]
        cal_end = layout["calibration"][1]

        calibration_data = modified[
            cal_start:cal_end + 1
        ]

        axis_candidates = self.map_detector.detect_axis_patterns(
            calibration_data
        )

        table_candidates = self.map_detector.detect_table_candidates(
            calibration_data
        )

        classification_summary = {
            "BOOT": 0,
            "CODE": 0,
            "CALIBRATION": 0,
            "CHECKSUM": 0,
            "UNKNOWN": 0
        }

        for cluster in clusters:

            classification = cluster.get(
                "classification",
                "UNKNOWN"
            )

            if classification in classification_summary:
                classification_summary[classification] += 1
            else:
                classification_summary["UNKNOWN"] += 1

        largest_cluster = max(
            [
                cluster["length"]
                for cluster in clusters
            ],
            default=0
        )

        address_stats = {
            "lowest_modified": min(
                [
                    cluster["start"]
                    for cluster in clusters
                ],
                default=0
            ),
            "highest_modified": max(
                [
                    cluster["end"]
                    for cluster in clusters
                ],
                default=0
            )
        }

        boot_clusters = [
            cluster
            for cluster in clusters
            if cluster["classification"] == "BOOT"
        ]

        boot_warning = len(boot_clusters) > 0

        changed_calibration_clusters = [
            cluster
            for cluster in clusters
            if cluster["classification"] == "CALIBRATION"
        ]

        filtered_tables = []

        seen_tables = set()

        for table in table_candidates:

            table_start = cal_start + table["address"]
            table_end = table_start + table["size"] - 1

            unique_key = (
                table_start,
                table["size"]
            )

            if unique_key in seen_tables:
                continue

            seen_tables.add(unique_key)

            for cluster in changed_calibration_clusters:

                if (
                    table_start <= cluster["end"]
                    and table_end >= cluster["start"]
                ):
                    filtered_tables.append(table)
                    break

        filtered_tables = self.shape_engine.classify_tables(
            filtered_tables
        )

        anomaly_report = {
            "anomaly_count": 0,
            "anomalies": []
        }

        for table in filtered_tables:

            matrix = self._build_matrix(
                table,
                calibration_data
            )

            if matrix is None:
                continue

            family = table.get(
                "family",
                "UNKNOWN"
            )

            self.anomaly_detector.detect_spikes(
                matrix,
                family
            )

            self.anomaly_detector.detect_gradient_breaks(
                matrix,
                family
            )

            if family == "DURATION":

                self.anomaly_detector.validate_injection_duration(
                    matrix,
                    family
                )

            if family == "RAIL_PRESSURE":

                self.anomaly_detector.validate_rail_pressure(
                    matrix
                )

        anomaly_report = self.anomaly_detector.export_results()

        family_summary = self.shape_engine.get_family_summary(
            filtered_tables
        )

        map_names = self.map_naming_engine.classify(
            filtered_tables
        )

        egr_analysis = self.egr_detector.detect(
            filtered_tables
        )

        dtc_analysis = self.dtc_detector.detect(
            changed_calibration_clusters
        )

        ranked_maps = self.map_ranker.rank_tables(
            filtered_tables,
            changed_calibration_clusters,
            cal_start
        )

        torque_tables = self.torque_structure_detector.classify_tables(
            ranked_maps,
            changed_calibration_clusters
        )

        torque_summary = self.torque_structure_detector.summarize(
            torque_tables
        )

        boost_tables = self.boost_detector.classify_tables(
            filtered_tables
        )

        boost_summary = self.boost_detector.summarize(
            boost_tables
        )

        rail_tables = self.rail_detector.classify_tables(
            filtered_tables
        )

        rail_summary = self.rail_detector.summarize(
            rail_tables
        )

        smoke_tables = self.smoke_detector.classify_tables(
            filtered_tables
        )

        smoke_summary = self.smoke_detector.summarize(
            smoke_tables
        )

        duration_maps = self.duration_detector.detect(
            filtered_tables
        )

        soi_maps = self.soi_detector.detect(
            filtered_tables
        )

        driver_wish_maps = self.driver_wish_detector.detect(
            filtered_tables
        )

        iq_nm_maps = self.iq_nm_detector.detect(
            filtered_tables
        )

        limiter_maps = self.limiter_stack_detector.detect(
            filtered_tables
        )

        control_chain = self.relationship_engine.build(
            driver_wish_maps,
            torque_tables,
            iq_nm_maps,
            limiter_maps,
            smoke_tables,
            duration_maps,
            rail_tables,
            boost_tables,
            soi_maps
        )

        confidence = self.confidence_engine.calculate(
            torque_tables
            + boost_tables
            + rail_tables
            + smoke_tables
            + duration_maps
            + soi_maps
            + driver_wish_maps
            + iq_nm_maps
            + limiter_maps
        )

        signature = self.signature_engine.detect(
            swid,
            torque_tables
        )

        correlated_maps = self.map_correlator.correlate(
            axis_candidates,
            torque_tables,
            cal_start
        )

        torque_relationships = self.torque_relationship_engine.build(
            driver_wish_maps,
            limiter_maps,
            torque_tables[:1] if torque_tables else []
        )

        fuel_relationships = self.fuel_relationship_engine.build(
            smoke_tables,
            duration_maps,
            rail_tables,
            iq_nm_maps
        )

        air_relationships = self.air_relationship_engine.build(
            boost_tables,
            [],
            []
        )

        export_summary = self.export_engine.export_summary(
            {
                "swid": swid,
                "processor_analysis": {
                    "cluster_count": len(clusters)
                },
                "map_ranking_summary": {
                    "detected_maps": len(filtered_tables)
                }
            }
        )

        torque_model_report = self.torque_model.analyze(
            driver_wish_maps,
            torque_tables,
            limiter_maps
        )

        fuel_model_report = self.fuel_model.analyze(
            smoke_tables,
            duration_maps,
            rail_tables,
            iq_nm_maps
        )

        air_model_report = self.air_model.analyze(
            boost_tables,
            [],
            []
        )

        interpolation_validation = self.interpolation_validator.validate(
            list(calibration_data)
        )

        map_similarity_score = 0
        if len(filtered_tables) > 1:
            map_similarity_score = self.similarity_engine.compare(
                filtered_tables[0],
                filtered_tables[1]
            )

        calibration_ranking = ranked_maps[:20]

        top_modified_clusters = sorted(
            changed_calibration_clusters,
            key=lambda x: x["length"],
            reverse=True
        )

        top_modified_clusters = [
            {
                "start": cluster["start"],
                "end": cluster["end"],
                "length": cluster["length"],
                "classification": cluster["classification"]
            }
            for cluster in top_modified_clusters[:20]
        ]

        dominant_cluster = None

        if top_modified_clusters:
            dominant_cluster = top_modified_clusters[0]

        calibration_bytes_modified = sum(
            cluster["length"]
            for cluster in changed_calibration_clusters
        )

        calibration_size = (
            cal_end
            - cal_start
            + 1
        )

        calibration_coverage = 0

        if calibration_size > 0:

            calibration_coverage = round(
                calibration_bytes_modified * 100 / calibration_size,
                4
            )

        calibration_histogram = {
            "0_5": 0,
            "6_8": 0,
            "9_16": 0,
            "17_32": 0,
            "33_64": 0,
            "65_plus": 0
        }

        for change in changes:

            address = change["address"]

            if not (
                cal_start <= address <= cal_end
            ):
                continue

            delta = abs(change["delta"])

            if delta <= 5:
                calibration_histogram["0_5"] += 1
            elif delta <= 8:
                calibration_histogram["6_8"] += 1
            elif delta <= 16:
                calibration_histogram["9_16"] += 1
            elif delta <= 32:
                calibration_histogram["17_32"] += 1
            elif delta <= 64:
                calibration_histogram["33_64"] += 1
            else:
                calibration_histogram["65_plus"] += 1

        map_modification_score = 0

        if len(filtered_tables) > 0:

            map_modification_score = round(
                len(changed_calibration_clusters) * 100 / len(filtered_tables),
                2
            )

        map_ranking_summary = {
            "detected_maps": len(filtered_tables),
            "modified_maps": len(
                [
                    m
                    for m in ranked_maps
                    if m.get("overlap_bytes", 0) > 0
                ]
            ),
            "highest_score": ranked_maps[0]["score"] if ranked_maps else 0
        }

        map_correlation = {
            "map_count": len(correlated_maps),
            "high_confidence_maps": len(
                [
                    m
                    for m in correlated_maps
                    if m.get("confidence", 0) >= 80
                ]
            )
        }

        calibration_families = {
            "duration_maps": len(duration_maps),
            "soi_maps": len(soi_maps),
            "driver_wish_maps": len(driver_wish_maps),
            "iq_nm_maps": len(iq_nm_maps),
            "limiter_maps": len(limiter_maps)
        }

        rail_safety_report = self.rail_safety.analyze(
            []
        )

        smoke_prediction_report = self.smoke_predictor.predict(
            0,
            1
        )

        return {
            "swid": swid,

            "processor_analysis": {
                "rom_size": filesize,
                "changed_regions": len(modified_regions),
                "cluster_count": len(clusters),
                "largest_cluster": largest_cluster
            },

            "boot_analysis": {
                "boot_clusters": len(boot_clusters),
                "boot_modified": boot_warning
            },

            "address_stats": address_stats,

            "classification_summary": classification_summary,

            "delta_stats": delta_stats,

            "delta_analysis": delta_analysis,

            "oem_validation": oem_validation,

            "region_density": density,

            "layout": layout,

            "shape_analysis": {
                "detected_shapes": len(filtered_tables),
                "family_breakdown": family_summary
            },

            "map_names": map_names,

            "egr_analysis": egr_analysis,

            "dtc_analysis": dtc_analysis,

            "anomaly_analysis": anomaly_report,

            "calibration_relationship": control_chain,

            "calibration_confidence": confidence,

            "denso_signature": signature,

            "torque_analysis": {
                "summary": torque_summary,
                "top_torque_maps": torque_tables[:20]
            },

            "boost_analysis": {
                "summary": boost_summary,
                "top_boost_maps": boost_tables[:20]
            },

            "rail_analysis": {
                "summary": rail_summary,
                "top_rail_maps": rail_tables[:20]
            },

            "smoke_analysis": {
                "summary": smoke_summary,
                "top_smoke_maps": smoke_tables[:20]
            },

            "calibration_families": calibration_families,

            "torque_model": torque_model_report,

            "fuel_model": fuel_model_report,

            "air_model": air_model_report,

            "interpolation_validation": interpolation_validation,

            "map_similarity_score": map_similarity_score,

            "calibration_analysis": {
                "changed_calibration_clusters": len(
                    changed_calibration_clusters
                ),
                "calibration_start": cal_start,
                "calibration_end": cal_end,
                "candidate_axes": len(axis_candidates),
                "candidate_tables": len(filtered_tables),
                "map_modification_score": map_modification_score,
                "coverage_percent": calibration_coverage
            },

            "calibration_delta_histogram": calibration_histogram,

            "map_ranking_summary": map_ranking_summary,

            "map_correlation": map_correlation,

            "map_candidates": {
                "axis_count": len(axis_candidates),
                "table_count": len(filtered_tables),
                "sample_axes": axis_candidates[:25],
                "sample_tables": filtered_tables[:25]
            },

            "control_chain": control_chain,

            "calibration_relationships": control_chain,

            "calibration_confidence_report": confidence,

            "export_summary": export_summary,

            "rail_safety": rail_safety_report,

            "smoke_prediction": smoke_prediction_report,

            "top_modified_maps": calibration_ranking,

            "top_correlated_maps": correlated_maps[:20],

            "top_modified_tables": calibration_ranking,

            "top_modified_clusters": top_modified_clusters,

            "dominant_cluster": dominant_cluster,

            "sample_clusters": clusters[:25]
        }