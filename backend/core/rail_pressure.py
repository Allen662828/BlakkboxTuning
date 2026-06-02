class RailPressureOptimizer:
    def smooth_pressure_curve(self, values):
        if len(values) < 3:
            return values

        optimized = values[:]

        for i in range(1, len(values) - 1):
            optimized[i] = round((values[i - 1] + values[i] + values[i + 1]) / 3, 2)

        return optimized

    def validate_pressure_limit(self, pressure):
        return pressure <= 240
