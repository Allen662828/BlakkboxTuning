class InjectionTimingValidator:
    def validate_timing_curve(self, values):
        if len(values) < 4:
            return False

        unstable = 0

        for i in range(1, len(values)):
            delta = abs(values[i] - values[i - 1])

            if delta > 8:
                unstable += 1

        return unstable <= 2

    def reduce_rattle_regions(self, values):
        corrected = values[:]

        for i in range(1, len(values) - 1):
            corrected[i] = round((values[i - 1] + values[i] + values[i + 1]) / 3, 2)

        return corrected
