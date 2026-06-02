class SWIDDetector:
    KNOWN_PREFIXES = [
        '89663',
        '89661',
        '1860',
        'MEC'
    ]

    def detect(self, filename):
        for prefix in self.KNOWN_PREFIXES:
            if prefix in filename:
                return {
                    'detected': True,
                    'sw_family': prefix
                }

        return {
            'detected': False,
            'sw_family': None
        }
