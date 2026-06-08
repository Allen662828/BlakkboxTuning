# soi_detector.py

class SOIDetector:

    def detect(self, maps):

        results = []

        for table in maps:

            score = 0

            if table.get("shape") == "3D":
                score += 30

            if table.get("size", 0) >= 128:
                score += 20

            if table.get("smooth_ratio", 0) > 0.90:
                score += 30

            if score >= 50:

                results.append({
                    **table,
                    "detector": "SOI",
                    "confidence": score
                })

        return sorted(
            results,
            key=lambda x: x["confidence"],
            reverse=True
        )