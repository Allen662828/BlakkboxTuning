class ChecksumFamilyDetector:
    SIGNATURES = {
        'SH7055': ['7055', 'denso'],
        'SH7058': ['7058', 'toyota'],
        'SH72531': ['72531'],
        'SH72543': ['72543']
    }

    def detect(self, metadata):
        text = str(metadata).lower()

        for family, signatures in self.SIGNATURES.items():
            for signature in signatures:
                if signature in text:
                    return {
                        'family': family,
                        'detected': True
                    }

        return {
            'family': 'unknown',
            'detected': False
        }
