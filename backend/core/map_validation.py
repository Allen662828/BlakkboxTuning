class MapValidation:
    def validate_axis_structure(self, axis):
        if len(axis) < 4:
            return False

        monotonic = all(axis[i] <= axis[i + 1] for i in range(len(axis) - 1))

        return monotonic

    def validate_table_interpolation(self, table):
        if len(table) < 4:
            return False

        discontinuities = 0

        for i in range(1, len(table)):
            delta = abs(table[i] - table[i - 1])

            if delta > 25:
                discontinuities += 1

        return discontinuities <= 2

    def combustion_safe(self, boost, rail, fuel):
        if boost > 285:
            return False

        if rail > 240:
            return False

        if fuel > 110:
            return False

        return True
