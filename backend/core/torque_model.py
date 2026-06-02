class TorqueModel:
    def identify_limiters(self, tables):
        limiters = []

        for table in tables:
            size = table.get('size', 0)

            if size >= 128:
                limiters.append({
                    'offset': table.get('offset'),
                    'type': 'torque_limiter_candidate'
                })

        return limiters

    def validate_hierarchy(self, driver_request, torque_limit):
        return driver_request <= torque_limit
