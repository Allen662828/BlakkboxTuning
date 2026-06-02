class DescriptorScanner:
    def __init__(self):
        self.minimum_pointer = 0x10000

    def scan(self, data):
        descriptors = []

        for offset in range(0, len(data) - 16, 2):
            x_size = data[offset]
            y_size = data[offset + 1]

            if 1 < x_size <= 32 and 1 < y_size <= 32:
                x_pointer = int.from_bytes(data[offset + 2:offset + 6], 'big', signed=False)
                y_pointer = int.from_bytes(data[offset + 6:offset + 10], 'big', signed=False)
                z_pointer = int.from_bytes(data[offset + 10:offset + 14], 'big', signed=False)

                valid = (
                    self.minimum_pointer <= x_pointer < len(data) and
                    self.minimum_pointer <= y_pointer < len(data) and
                    self.minimum_pointer <= z_pointer < len(data)
                )

                if valid:
                    descriptors.append({
                        'offset': hex(offset),
                        'x_size': x_size,
                        'y_size': y_size,
                        'x_pointer': hex(x_pointer),
                        'y_pointer': hex(y_pointer),
                        'z_pointer': hex(z_pointer)
                    })

        return descriptors
