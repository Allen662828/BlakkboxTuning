class SH705xDecoder:
    PROCESSORS = [
        'SH7055',
        'SH7058',
        'SH72531',
        'SH72543'
    ]

    def detect_processor(self, filesize):
        if filesize <= 524288:
            return 'SH7055'

        if filesize <= 1048576:
            return 'SH7058'

        if filesize <= 2097152:
            return 'SH72531'

        return 'SH72543'

    def estimate_map_regions(self, filesize):
        return {
            'boot_region': [0x000000, 0x00FFFF],
            'code_region': [0x010000, int(filesize * 0.55)],
            'map_region': [int(filesize * 0.55), filesize]
        }
