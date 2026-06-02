class DensoChecksum:
    @staticmethod
    def simple_sum(data: bytes):
        checksum = 0

        for i in range(0, len(data), 2):
            word = int.from_bytes(data[i:i+2], 'big', signed=False)
            checksum = (checksum + word) & 0xFFFFFFFF

        return (~checksum) & 0xFFFFFFFF
