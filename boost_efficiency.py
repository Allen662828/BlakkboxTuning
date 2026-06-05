"""Boost efficiency balancer module."""


class BoostEfficiencyBalancer:
    """Balances boost values and validates spool rates."""

    def balance(self, boost_values):
        """Balance boost values by capping at 285."""
        balanced = []

        for value in boost_values:
            if value > 285:
                balanced.append(285)
            else:
                balanced.append(value)

        return balanced

    def validate_spool_rate(self, current, previous):
        """Validate spool rate doesn't exceed maximum delta of 18."""
        delta = current - previous

        return delta <= 18
