"""Validation configuration manager."""
import yaml
from pathlib import Path


class ValidationManager:
    """Manages validation modes and configuration."""

    def __init__(self, config_path='config/validation_modes.yaml'):
        """Initialize validation manager with configuration path."""
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        """Load validation configuration from YAML file."""
        if not self.config_path.exists():
            return {}

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_mode(self, mode='balanced'):
        """Get validation mode configuration."""
        modes = self.config.get('validation_modes', {})
        return modes.get(mode, {})

    def export_allowed(self, mode='balanced'):
        """Check if export is allowed on warning for given mode."""
        config = self.get_mode(mode)
        return config.get('export_allowed_on_warning', False)

    def preserve_oem_regions(self, mode='balanced'):
        """Check if OEM regions should be preserved for given mode."""
        config = self.get_mode(mode)
        return config.get('preserve_oem_regions', True)

    def checksum_required(self):
        """Check if checksum is required for minimum protection."""
        minimum = self.config.get('minimum_protection', {})
        return minimum.get('checksum_presence_required', True)
