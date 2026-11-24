"""Local lexical retrieval with explicit abstention. No generative model."""
import json,re,time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SupportEngine:
    def __init__(self,path=None,threshold=0.17):
        path=path or Path(__file__).resolve().parents[1]/'data/policies.json'
        self.documents=json.loads(Path(path).read_text())
        if not self.documents:raise ValueError('Knowledge base must not be empty')
        self.threshold=threshold
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words='english',sublinear_tf=True)
        self.matrix=self.vectorizer.fit_transform([d['title']+' '+d['text'] for d in self.documents])

    def answer(self,question):
        start=time.perf_counter(); trace=['validate']
        base={'answer':None,'citations':[],'score':0.0,'knowledge_version':'2026-11-24'}
        # Illustrative pattern guard only. Not a complete prompt-injection/security detector.
        if re.search(r'ignore.{0,30}(instructions|rules)|reveal.{0,30}(secret|system prompt)|api[_ -]?key|credit card number|password is|otp is',question,re.I):
            result=dict(base,status='blocked',message='Do not share secrets. This demo only answers store policy questions.');trace+=['safety_guard','stop']
        elif re.search(r'^(cancel|refund|delete|change|place|pay) (my|this|the) ',question,re.I):
            result=dict(base,status='handoff',message='This read-only service cannot take account or order actions. Use the secure account page.');trace+=['action_boundary','human_handoff']
        else:
            trace.append('retrieve');scores=cosine_similarity(self.vectorizer.transform([question]),self.matrix)[0];rank=sorted(range(len(scores)),key=lambda i:float(scores[i]),reverse=True);best=rank[0];score=float(scores[best]);second=float(scores[rank[1]]) if len(rank)>1 else 0
            base['score']=round(score,4)
            if score<self.threshold or (score-second<0.025 and score<0.3):
                result=dict(base,status='abstained',message='I cannot find a clear answer in the demo policy. Please contact support.');trace+=['confidence_gate','human_handoff']
            else:
                doc=self.documents[best];result=dict(base,status='answered',answer=doc['text'],citations=[{k:doc[k] for k in ['id','title','source','version']}],message='Exact policy excerpt, not a generated answer.');trace+=['confidence_gate','cite_exact_excerpt']
        result['trace']=trace;result['latency_ms']=round(1000*(time.perf_counter()-start),2);return result
