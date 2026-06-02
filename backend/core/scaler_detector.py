class ScalerDetector:
    KNOWN_SCALERS = {
        'rpm': [0.25, 0.5, 1, 2, 4],
        'boost': [0.01, 0.1, 1],
        'rail': [0.1, 1, 10],
        'fuel': [0.01, 0.1, 1]
    }

    def detect(self, values):
        detected = []

        for category, scalers in self.KNOWN_SCALERS.items():
            for scaler in scalers:
                scaled = [round(v * scaler, 2) for v in values[:8]]

                if self.validate_range(category, scaled):
                    detected.append({
                        'category': category,
                        'scaler': scaler,
                        'preview': scaled
                    })

        return detected

    def validate_range(self, category, values):
        if category == 'rpm':
            return max(values) <= 6000

        if category == 'boost':
            return max(values) <= 350

        if category == 'rail':
            return max(values) <= 2500

        if category == 'fuel':
            return max(values) <= 150

        return False
