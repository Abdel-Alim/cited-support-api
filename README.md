# Cited Support API

A local English support-policy retrieval API with citations, abstention, read-only action boundaries and an observable routing trace. FastAPI + scikit-learn TF-IDF + cosine similarity.

**AI-assisted portfolio project, November2026. Fictional demo policies. Not an LLM, multi-agent system, production service or client engagement.** The implementation was generated and tested with AI assistance. The candidate should study it and make changes before claiming independent mastery.

![API demo](docs/screenshot.png)

## Run

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
python evaluate.py
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the UI, `/docs` for the OpenAPI interface, `/health` for liveness. Python3.10 or later.

```sh
curl -X POST http://127.0.0.1:8000/answer -H 'Content-Type: application/json' -d '{"question":"How long is the electronics warranty?"}'
```

Docker: `docker build -t cited-support .` and `docker run --rm -p 8000:8000 cited-support`. The Dockerfile uses a non-root user; the Docker image itself is supplied but not runtime-tested here.

## Architecture and tradeoffs

```text
POST /answer -> validated request -> illustrative pattern guard
                                  -> account-action handoff
                                  -> TF-IDF retrieval -> score/ambiguity gate -> cited exact excerpt
                                                                         -> abstention
```

There are10 authored policy documents. A word unigram/bigram index retrieves by cosine similarity. The highest result must pass a0.17 score threshold and a small ambiguity margin before the exact document text is returned with its ID, title, version and demo-policy reference. These are local identifiers, not clickable external source URLs. There is no generated synthesis, so the service cannot invent a new policy sentence. It can still retrieve a wrong policy. The score is not a calibrated probability.

A lexical baseline is cheap, deterministic and testable. It does not prove semantic embedding, vector database or LLM orchestration experience. Those are explicit future extensions, not current claims. No external key or network call is needed.

## Verified evidence

- 12 tests pass: request validation, health, citations, exact source-excerpt consistency, abstention, guard behavior, read-only boundary and regression coverage.
- 23/24 manually authored English evaluation cases meet both expected route and expected document. Full results in `reports/evaluation.json`.
- Known failure retained: 'Where is order tracking after dispatch?' abstains because shipping and address policy scores are close. This is safer than confidently returning the wrong policy, but is still a failed expected-answer case.
- Browser checks exercise cited answer, unknown-question abstention, action handoff, desktop/mobile layout and no page errors.

This24-case set is developer-authored and small, not independent, adversarially complete or representative of real customer traffic. Thresholds are demo choices, not a held-out calibrated guarantee. No production accuracy claim is made.

## Safety and deployment limits

The pattern guard catches a few obvious secret/instruction phrases. It is illustrative, not a prompt-injection defense or data-loss-prevention system. The service has no tools to mutate accounts or send data elsewhere. It does not persist questions, but hosting infrastructure may log requests. Do not enter real private information. Before real deployment add authentication, rate limiting, input/output review, telemetry with redaction, larger independent evaluation, policy ownership and security review. This demo serves English questions only.

## Project map

- `app/engine.py`: retrieval and routing.
- `app/main.py`: typed API and static UI.
- `data/policies.json`: fictional local knowledge base.
- `data/evaluation.json`: developer-authored regression questions.
- `evaluate.py`: reproducible evaluator which retains failures.
- `tests/`: API and invariant tests.
- `docs/WALKTHROUGH.ar.md`: Arabic interview study guide.

## Requirement mapping

Forsa asks Python,LLMs,RAG,embeddings and agent frameworks. This project only demonstrates the retrieval/API/evaluation baseline, while existing MarketAgent demonstrates a separate LangGraph workflow. Beseha asks useful automation,Git,tests,documentation andAPI integration. Do not represent either demo as production experience.

- https://forsaprop.com/en/careers/agentic-ai-engineer/
- https://beseha.com/careers/jobs/tech-data-automation-intern-beseha-academy/
- https://fastapi.tiangolo.com/tutorial/testing/
- https://scikit-learn.org/stable/modules/feature_extraction.html
