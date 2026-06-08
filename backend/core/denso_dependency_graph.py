class DensoDependencyGraph:

    def build(
        self,
        torque_maps,
        fuel_maps,
        air_maps
    ):

        nodes = []
        edges = []

        for m in torque_maps:

            nodes.append({

                "name":
                    m.get(
                        "name",
                        "TORQUE"
                    ),

                "type":
                    "TORQUE"
            })

        for m in fuel_maps:

            nodes.append({

                "name":
                    m.get(
                        "name",
                        "FUEL"
                    ),

                "type":
                    "FUEL"
            })

        for m in air_maps:

            nodes.append({

                "name":
                    m.get(
                        "name",
                        "AIR"
                    ),

                "type":
                    "AIR"
            })

        for torque in torque_maps:

            for fuel in fuel_maps:

                edges.append({

                    "source":
                        torque.get(
                            "name"
                        ),

                    "target":
                        fuel.get(
                            "name"
                        ),

                    "relationship":
                        "TORQUE_TO_FUEL"
                })

        for fuel in fuel_maps:

            for air in air_maps:

                edges.append({

                    "source":
                        fuel.get(
                            "name"
                        ),

                    "target":
                        air.get(
                            "name"
                        ),

                    "relationship":
                        "FUEL_TO_AIR"
                })

        return {

            "nodes":
                nodes,

            "edges":
                edges
        }