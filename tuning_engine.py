"""
tuning_engine.py
"""

from .bin_comparator import BinComparator
from .region_classifier import RegionClassifier
from .delta_analyzer import DeltaAnalyzer
from .blakkbox_filter_engine import BlakkboxFilterEngine
from .oem_validator import OEMValidator


class BlakkboxTuningEngine:

    def __init__(self):

        self.delta_analyzer = (
            DeltaAnalyzer()
        )

        self.filter_engine = (
            BlakkboxFilterEngine()
        )

        self.oem_validator = (
            OEMValidator()
        )

    def analyze(
        self,
        original,
        modified
    ):

        filesize = len(original)

        #
        # Comparator
        #

        comparator = BinComparator(
            original,
            modified
        )

        #
        # Raw byte changes
        #

        changes = (
            comparator.compare_bytes()
        )

        #
        # Modified regions
        #

        modified_regions = (
            comparator.find_modified_regions()
        )

        #
        # Cluster regions
        #

        clusters = (
            comparator.cluster_changes()
        )

        #
        # Statistics
        #

        delta_stats = (
            comparator.calculate_delta_stats()
        )

        #
        # Region classification
        #

        classifier = (
            RegionClassifier(
                filesize
            )
        )

        modified_regions = (
            classifier.classify_regions(
                modified_regions
            )
        )

        clusters = (
            classifier.classify_regions(
                clusters
            )
        )

        #
        # Delta analysis
        #

        delta_analysis = (
            self.delta_analyzer.analyze(
                changes
            )
        )

        #
        # BLAKKBOX filter
        #

        filtered_changes = (
            self.filter_engine.filter_changes(
                changes
            )
        )

        filter_summary = (
            self.filter_engine.summarize(
                filtered_changes
            )
        )

        #
        # OEM validation
        #

        oem_validation = (
            self.oem_validator.validate(
                original,
                modified,
                modified_regions
            )
        )

        #
        # Classification summary
        #

        summary = {

            "BOOT": 0,
            "CODE": 0,
            "CALIBRATION": 0,
            "CHECKSUM": 0,
            "UNKNOWN": 0
        }

        for cluster in clusters:

            region_type = (
                cluster.get(
                    "classification",
                    "UNKNOWN"
                )
            )

            if region_type in summary:

                summary[
                    region_type
                ] += 1

            else:

                summary[
                    "UNKNOWN"
                ] += 1

        #
        # Largest modified region
        #

        largest_region = max(

            [
                region["length"]
                for region
                in modified_regions
            ],

            default=0
        )

        #
        # Final result
        #

        return {

            "processor_analysis": {

                "rom_size":
                    filesize,

                "changed_regions":
                    len(
                        modified_regions
                    ),

                "cluster_count":
                    len(
                        clusters
                    ),

                "largest_region":
                    largest_region
            },

            "classification_summary":
                summary,

            "delta_stats":
                delta_stats,

            "delta_analysis":
                delta_analysis,

            "filter_summary":
                filter_summary,

            "oem_validation":
                oem_validation,

            "layout":
                classifier.get_layout(),

            "sample_clusters":
                clusters[:25]
        }