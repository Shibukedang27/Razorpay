from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from .models import CartEvent
from .engine import decide, simulate_outcome

app = FastAPI(title='RazorFlow AI', version='1.0.0')
ROOT = Path(__file__).resolve().parent.parent
AUDIT=[]

@app.get('/health')
def health():
    return {'status':'ok','service':'razorflow-ai'}

@app.post('/api/decide')
def make_decision(event: CartEvent):
    d = decide(event)
    o = simulate_outcome(event, d)
    record={'event':event.model_dump(),'decision':d.model_dump(),'outcome':o.model_dump()}
    AUDIT.append(record)
    return record

@app.get('/api/audit')
def audit():
    return {'count':len(AUDIT),'records':AUDIT[-100:]}

@app.get('/')
def root():
    return FileResponse(ROOT/'static'/'index.html')
