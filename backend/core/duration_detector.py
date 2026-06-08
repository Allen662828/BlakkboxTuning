# duration_detector.py

class DurationDetector:

    def detect(self, maps):

        results = []

        for table in maps:

            score = 0

            if table.get("shape") == "3D":
                score += 25

            if table.get("size", 0) >= 256:
                score += 25

            if table.get("family") == "SMOOTH_SURFACE":
                score += 25

            if score >= 50:

                results.append({
                    **table,
                    "detector": "DURATION",
                    "confidence": score
                })

        return sorted(
            results,
            key=lambda x: x["confidence"],
            reverse=True
        )