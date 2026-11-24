import json
from pathlib import Path
from app.engine import SupportEngine

def evaluate():
    engine=SupportEngine();results=[]
    for row in json.loads(Path('data/evaluation.json').read_text()):
        answer=engine.answer(row['question']);actual=answer['citations'][0]['id'] if answer['citations'] else None
        passed=answer['status']==row['expected_status'] and actual==row['expected_document']
        results.append(dict(row,actual_status=answer['status'],actual_document=actual,score=answer['score'],passed=passed))
    report={'dataset':'24 manually authored English demo cases, not independent or production evaluation','passed':sum(r['passed'] for r in results),'total':len(results),'results':results}
    Path('reports').mkdir(exist_ok=True);Path('reports/evaluation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));return report
if __name__=='__main__':evaluate()
