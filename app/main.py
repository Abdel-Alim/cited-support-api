from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from app.engine import SupportEngine

app=FastAPI(title='Cited Support API',version='0.1.0',description='Read-only lexical retrieval demo. Synthetic policies. No LLM, no account actions.')
engine=SupportEngine()
class Question(BaseModel):
    question:str=Field(min_length=3,max_length=1000)
@app.get('/health')
def health():return {'status':'ok','documents':len(engine.documents),'mode':'local-tfidf-extractive'}
@app.post('/answer')
def answer(body:Question):return engine.answer(body.question)
@app.get('/')
def home():return FileResponse(Path(__file__).parent/'static/index.html')
