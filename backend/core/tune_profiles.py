class TuneProfiles:
    PROFILES = {
        'economy': {
            'boost_factor': 1.02,
            'fuel_factor': 1.01,
            'rail_factor': 1.01
        },
        'sport': {
            'boost_factor': 1.05,
            'fuel_factor': 1.04,
            'rail_factor': 1.03
        },
        'aggressive': {
            'boost_factor': 1.08,
            'fuel_factor': 1.07,
            'rail_factor': 1.05
        },
        'maxout': {
            'boost_factor': 1.10,
            'fuel_factor': 1.09,
            'rail_factor': 1.07
        }
    }

    def get_profile(self, profile_name):
        return self.PROFILES.get(profile_name)
