# iq_nm_detector.py

class IQNmDetector:

    def detect(self, maps):

        results = []

        for table in maps:

            score = 0

            if table.get("shape") == "2D":
                score += 25

            if table.get("family") == "LINEAR":
                score += 35

            if table.get("size", 0) <= 128:
                score += 20

            if score >= 50:

                results.append({
                    **table,
                    "detector": "IQ_TO_NM",
                    "confidence": score
                })

        return sorted(
            results,
            key=lambda x: x["confidence"],
            reverse=True
        )