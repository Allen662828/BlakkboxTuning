"""FastAPI application for BlakkboxTuning API."""
from fastapi import FastAPI, UploadFile

app = FastAPI(title='BlakkboxTuning API')


@app.get('/')
def root():
    """Health check endpoint."""
    return {
        'status': 'online',
        'platform': 'BlakkboxTuning'
    }


@app.post('/analyze')
async def analyze(original: UploadFile, mod: UploadFile):
    """Analyze original and modified tuning files."""
    return {
        'original': original.filename,
        'mod': mod.filename,
        'status': 'queued'
    }
