class ModRebuilder:

    def rebuild(
        self,
        original,
        filtered_changes
    ):

        output = bytearray(
            original
        )

        for change in filtered_changes:

            address = (
                change["address"]
            )

            value = (
                original[address]
                +
                change["filtered_delta"]
            )

            value = max(
                0,
                min(255, value)
            )

            output[address] = value

        return bytes(output)