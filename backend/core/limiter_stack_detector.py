# limiter_stack_detector.py

class LimiterStackDetector:

    def detect(self, maps):

        results = []

        for table in maps:

            score = 0

            if table.get("shape") == "2D":
                score += 20

            if table.get("family") in [
                "RAMP",
                "LINEAR"
            ]:
                score += 40

            if table.get("size", 0) <= 256:
                score += 20

            if score >= 50:

                results.append({
                    **table,
                    "detector": "LIMITER",
                    "confidence": score
                })

        return sorted(
            results,
            key=lambda x: x["confidence"],
            reverse=True
        )