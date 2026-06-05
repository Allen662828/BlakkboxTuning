class MapDetector:
    def detect_axis_patterns(self, data):
        patterns = []

        for i in range(0, len(data) - 32):
            block = data[i:i+16]

            ascending = all(block[x] <= block[x + 1] for x in range(len(block) - 1))

            if ascending:
                patterns.append({
                    'offset': hex(i),
                    'type': 'axis_candidate'
                })

        return patterns

    def detect_table_candidates(self, data):
        tables = []

        for i in range(0, len(data) - 256, 16):
            segment = data[i:i+256]
            unique_ratio = len(set(segment)) / max(len(segment), 1)

            if 0.15 < unique_ratio < 0.85:
                tables.append({
                    'offset': hex(i),
                    'size': len(segment),
                    'type': 'table_candidate'
                })

        return tables
