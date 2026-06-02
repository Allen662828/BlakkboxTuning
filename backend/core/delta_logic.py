class BlakkboxDeltaLogic:
    def __init__(self):
        self.keep_threshold = 5
        self.medium_threshold = 8

    def process_delta(self, delta):
        abs_delta = abs(delta)

        if abs_delta <= self.keep_threshold:
            return delta

        if abs_delta <= self.medium_threshold:
            return round(delta * 0.80, 2)

        return round(delta * 0.55, 2)

    def smooth_sequence(self, values):
        if len(values) < 3:
            return values

        smoothed = values[:]

        for i in range(1, len(values) - 1):
            prev_v = values[i - 1]
            curr_v = values[i]
            next_v = values[i + 1]

            if abs(curr_v - prev_v) > 10 and abs(curr_v - next_v) > 10:
                smoothed[i] = round((prev_v + next_v) / 2, 2)

        return smoothed
