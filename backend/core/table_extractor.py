class TableExtractor:
    def __init__(self):
        self.minimum_axis_length = 8
        self.minimum_table_size = 16

    def is_monotonic(self, values):
        return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

    def detect_axes(self, data):
        axes = []

        for offset in range(0, len(data) - 64):
            block = list(data[offset:offset + 16])

            if self.is_monotonic(block):
                axes.append({
                    'offset': hex(offset),
                    'length': len(block),
                    'values': block,
                    'type': 'axis_candidate'
                })

        return axes

    def detect_tables(self, data):
        tables = []

        for offset in range(0, len(data) - 512, 16):
            segment = data[offset:offset + 256]
            unique_ratio = len(set(segment)) / len(segment)

            if 0.20 <= unique_ratio <= 0.85:
                tables.append({
                    'offset': hex(offset),
                    'size': len(segment),
                    'unique_ratio': round(unique_ratio, 3),
                    'type': 'table_candidate'
                })

        return tables
