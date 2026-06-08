from fastapi import FastAPI, UploadFile, File, HTTPException

from backend.core.tuning_engine import (
    BlakkboxTuningEngine
)

app = FastAPI(
    title="DENSO ROM STUDIO"
)

engine = (
    BlakkboxTuningEngine()
)


@app.get("/")
def root():

    return {
        "status": "online"
    }


@app.post("/analyze")
async def analyze(

    original: UploadFile = File(...),
    modified: UploadFile = File(...)

):

    original_bytes = (
        await original.read()
    )

    modified_bytes = (
        await modified.read()
    )

    try:
        result = engine.analyze(

            original_bytes,
            modified_bytes,
            original.filename

        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {

        "status":
            "complete",

        "original":
            original.filename,

        "modified":
            modified.filename,

        "analysis":
            result
    }
