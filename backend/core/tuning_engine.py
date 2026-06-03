"""Blakkbox tuning analysis engine."""
from .table_extractor import TableExtractor
from .refinement_engine import RefinementEngine
from .checksum_rebuilder import ChecksumRebuilder
from .classifiers import CalibrationClassifier
from .sh705x_decoder import SH705xDecoder


class BlakkboxTuningEngine:
    """Engine for analyzing and processing tuning files."""

    def __init__(self):
        """Initialize tuning engine with all components."""
        self.extractor = TableExtractor()
        self.refiner = RefinementEngine()
        self.checksum = ChecksumRebuilder()
        self.classifier = CalibrationClassifier()
        self.decoder = SH705xDecoder()

    def analyze(self, original, modified):
        """Analyze tuning file differences and detect processor information."""
        filesize = len(original)

        return {
            'processor': self.decoder.detect_processor(filesize),
            'regions': self.decoder.estimate_map_regions(filesize),
            'axes': self.extractor.detect_axes(modified),
            'tables': self.extractor.detect_tables(modified),
            'checksum': self.checksum.rebuild(modified)
        }
