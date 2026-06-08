class AutomaticMapRenamer:

    def rename(
        self,
        tables
    ):

        counter = {}

        output = []

        for table in tables:

            family = table.get(
                "family",
                "UNKNOWN"
            )

            counter[family] = (

                counter.get(
                    family,
                    0
                )

                + 1
            )

            table["name"] = (

                f"{family}_"

                f"{counter[family]}"
            )

            output.append(
                table
            )

        return output