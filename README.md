# RazorFlow AI

RazorFlow AI is my Razorpay AI Buildathon 2026 project for **Track 1 — AI Growth & Agentic Commerce**.

The idea is simple: an ecommerce merchant often knows a cart is at risk, but deciding what to do next is still manual or rule-heavy. RazorFlow looks at a small set of cart and customer signals, chooses one bounded action, checks that action against deterministic safety rules, and records what happened.

I deliberately kept the first version small enough to understand end-to-end instead of turning it into a generic chatbot.

## What the system actually does

For each cart event the backend:

1. reads cart value, idle time, customer history, discount sensitivity, product affinity, recent payment failures and inventory risk;
2. estimates whether there is a useful recovery/growth opportunity;
3. chooses one action such as a recommendation, reminder, coupon proposal, stop, or human review;
4. passes that action through a deterministic policy layer;
5. returns the decision, reason, confidence and approval state;
6. records the decision in the audit endpoint;
7. evaluates the same policy over a reproducible synthetic batch.

The important design choice is that the decision layer and the execution/safety layer are separate. A model or agent can suggest an action, but it does not get unrestricted authority over money-related actions.

## Safety rules in this prototype

- coupon proposals are approval-gated;
- repeated payment failures are sent to human review;
- high inventory uncertainty is sent to human review;
- stale carts trigger a stopping rule;
- every decision has a reason and confidence value;
- the current demo uses synthetic data only and does not move real money.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python data/generate.py
python evaluate.py
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Tests

```bash
pytest -q
```

Current local result: **7/7 tests pass**.

The GitHub Actions workflow regenerates the dataset, runs the tests and reruns evaluation so the committed numbers are reproducible.

## Evaluation

I used 250 deterministic synthetic cart records generated with seed 42. On this simulation:

- baseline conversions: **34**
- policy-agent conversions: **45**
- simulated conversion uplift: **32.35%**
- baseline revenue: **₹129,055.60**
- policy-agent revenue: **₹176,224.83**
- simulated revenue uplift: **36.55%**
- simulated incremental recovered revenue: **₹47,169.23**
- approval-gated actions: **88**
- stopping-rule actions: **68**

These numbers are **synthetic simulation results, not production claims**. I included them because the track asks for measurable value, but a real merchant deployment would need live A/B testing before making any revenue-uplift claim.

## Why synthetic data

I did not want to use real customer or payment data for a buildathon prototype. `data/generate.py` creates the dataset used by the tests and evaluation. It contains no real identities, cards, payment credentials or merchant data.

## Project structure

- `app/` — FastAPI endpoints, typed models and decision/policy engine
- `data/` — deterministic synthetic-data generator
- `tests/` — policy and API tests
- `docs/` — architecture, API notes, evaluation output and build notes
- `static/` — simple merchant-facing demo page
- `.github/workflows/ci.yml` — reproducible CI validation

## What I would improve next

The current policy engine is intentionally deterministic so that its behaviour can be tested and explained. The next useful step would be to replace only the opportunity-scoring component with a trained model, keep the deterministic safety gate unchanged, and evaluate it on a proper held-out dataset. After that I would connect the approved action layer to Razorpay Test Mode and run a controlled experiment rather than relying on simulated uplift.

More implementation notes and trade-offs are in `docs/BUILD_NOTES.md`.
