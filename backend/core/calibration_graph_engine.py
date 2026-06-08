class CalibrationGraphEngine:

    def build(
        self,
        relationships
    ):

        nodes = set()

        edges = []

        for relation in relationships:

            source = relation["source"]
            target = relation["target"]

            nodes.add(source)
            nodes.add(target)

            edges.append({

                "from":
                    source,

                "to":
                    target
            })

        return {

            "nodes":
                sorted(
                    list(nodes)
                ),

            "edges":
                edges
        }