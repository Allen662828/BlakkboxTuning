from fastapi import FastAPI, UploadFile

app = FastAPI(title='BlakkboxTuning API')

@app.get('/')
def root():
    return {
        'status': 'online',
        'platform': 'BlakkboxTuning'
    }

@app.post('/analyze')
async def analyze(original: UploadFile, mod: UploadFile):
    return {
        'original': original.filename,
        'mod': mod.filename,
        'status': 'queued'
    }
