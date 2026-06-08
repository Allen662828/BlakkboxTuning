# driver_wish_detector.py

class DriverWishDetector:

    def detect(self, maps):

        results = []

        for table in maps:

            score = 0

            if table.get("shape") == "2D":
                score += 20

            if table.get("size", 0) in [128, 256]:
                score += 30

            if table.get("family") == "RAMP":
                score += 30

            if score >= 50:

                results.append({
                    **table,
                    "detector": "DRIVER_WISH",
                    "confidence": score
                })

        return sorted(
            results,
            key=lambda x: x["confidence"],
            reverse=True
        )