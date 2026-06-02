class SmokeLimiterSynchronization:
    def synchronize(self, fuel_table, air_table):
        synchronized = []

        for fuel, air in zip(fuel_table, air_table):
            if air == 0:
                ratio = 0
            else:
                ratio = fuel / air

            synchronized.append({
                'fuel': fuel,
                'air': air,
                'afr_ratio': round(ratio, 4)
            })

        return synchronized

    def validate_smoke_threshold(self, afr_ratio):
        return afr_ratio < 0.065
