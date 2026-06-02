class ChecksumRebuilder:
    def __init__(self):
        self.supported_families = [
            'SH7055',
            'SH7058',
            'SH72531',
            'SH72543'
        ]

    def calculate_sum32(self, data, start=0, end=None):
        if end is None:
            end = len(data)

        checksum = 0

        for i in range(start, end, 2):
            word = int.from_bytes(data[i:i+2], 'big', signed=False)
            checksum = (checksum + word) & 0xFFFFFFFF

        return checksum

    def invert_checksum(self, checksum):
        return (~checksum) & 0xFFFFFFFF

    def rebuild(self, data):
        raw = self.calculate_sum32(data)

        return {
            'raw_checksum': raw,
            'rebuilt_checksum': self.invert_checksum(raw)
        }
