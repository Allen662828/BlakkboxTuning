class SafetyFilters:
    PROTECTED_KEYWORDS = [
        'EGR',
        'DTC',
        'ZERO_GROUP'
    ]

    def preserve_zero_groups(self, changes):
        filtered = []

        for change in changes:
            protected = False

            for keyword in self.PROTECTED_KEYWORDS:
                if keyword in str(change):
                    protected = True
                    break

            if not protected:
                filtered.append(change)

        return filtered

    def validate_limits(self, boost, rail, fuel):
        warnings = []

        if boost > 300:
            warnings.append('BOOST_LIMIT_EXCEEDED')

        if rail > 250:
            warnings.append('RAIL_PRESSURE_EXCEEDED')

        if fuel > 120:
            warnings.append('FUEL_LIMIT_EXCEEDED')

        return warnings
