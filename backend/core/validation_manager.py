import yaml
from pathlib import Path

class ValidationManager:
    def __init__(self, config_path='config/validation_modes.yaml'):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            return {}

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_mode(self, mode='balanced'):
        modes = self.config.get('validation_modes', {})
        return modes.get(mode, {})

    def export_allowed(self, mode='balanced'):
        config = self.get_mode(mode)
        return config.get('export_allowed_on_warning', False)

    def preserve_oem_regions(self, mode='balanced'):
        config = self.get_mode(mode)
        return config.get('preserve_oem_regions', True)

    def checksum_required(self):
        minimum = self.config.get('minimum_protection', {})
        return minimum.get('checksum_presence_required', True)
