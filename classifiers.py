class CalibrationClassifier:
    TORQUE_KEYWORDS = ['torque', 'limit', 'driver']
    BOOST_KEYWORDS = ['boost', 'turbo', 'map']
    SMOKE_KEYWORDS = ['smoke', 'afr', 'lambda']

    def classify(self, candidate):
        name = candidate.get('name', '').lower()

        for keyword in self.TORQUE_KEYWORDS:
            if keyword in name:
                return 'torque'

        for keyword in self.BOOST_KEYWORDS:
            if keyword in name:
                return 'boost'

        for keyword in self.SMOKE_KEYWORDS:
            if keyword in name:
                return 'smoke'

        return 'unknown'
