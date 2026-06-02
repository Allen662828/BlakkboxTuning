class BoostEfficiencyBalancer:
    def balance(self, boost_values):
        balanced = []

        for value in boost_values:
            if value > 285:
                balanced.append(285)
            else:
                balanced.append(value)

        return balanced

    def validate_spool_rate(self, current, previous):
        delta = current - previous

        return delta <= 18
