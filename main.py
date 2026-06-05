from __future__ import annotations

import time
import traceback

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.core.swid_detector import SWIDDetector
from backend.core.tuning_engine import BlakkboxTuningEngine

app = FastAPI(
    title="BlakkboxTuning API",
    version="0.2.0",
    description="DENSO Smart Delta Analysis Engine"
)

print("[BOOT] Initializing Blakkbox Engine...")

engine = BlakkboxTuningEngine()
swid_detector = SWIDDetector()

print("[BOOT] Engine Ready")


@app.get("/")
def root():
    return {
        "status": "online",
        "platform": "BlakkboxTuning",
        "engine": "ready"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
def version():
    return {
        "name": "BlakkboxTuning",
        "version": "0.2.0"
    }


@app.post("/analyze")
async def analyze(
    original: UploadFile = File(...),
    mod: UploadFile = File(...)
):
    request_start = time.time()

    try:

        print("\n==============================")
        print("NEW ANALYSIS REQUEST")
        print("==============================")

        original_bytes = await original.read()
        mod_bytes = await mod.read()

        print(f"Original : {original.filename}")
        print(f"Modified : {mod.filename}")

        print(f"Original Size : {len(original_bytes):,}")
        print(f"Modified Size : {len(mod_bytes):,}")

        if len(original_bytes) != len(mod_bytes):
            raise HTTPException(
                status_code=400,
                detail="original and mod must have identical size"
            )

        print("\n[STEP 1] SWID Detection")

        swid = swid_detector.detect(
            original.filename or mod.filename or "",
            data=original_bytes
        )

        print("[OK] SWID completed")

        print("\n[STEP 2] Analysis Engine")

        analysis = engine.analyze(
            original_bytes,
            mod_bytes
        )

        print("[OK] Analysis completed")

        result = {
            "status": "complete",
            "execution_time_sec": round(
                time.time() - request_start,
                3
            ),
            "original": original.filename,
            "mod": mod.filename,
            "swid": swid,
            "analysis": analysis
        }

        print("\nRESULT:")
        print(result)

        return result

    except HTTPException:
        raise

    except Exception as exc:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(exc),
                "type": type(exc).__name__
            }
        )