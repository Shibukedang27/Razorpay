# Build notes

These are the main choices I made while building the prototype and the reasons behind them.

## 1. Keep the first version deterministic

For a payments/commerce project, I preferred a decision path I could reproduce exactly. The current engine uses explicit thresholds instead of hiding every decision inside an LLM call. This makes tests, failure cases and audit logs easier to reason about.

The architecture still leaves a clear place for ML: opportunity scoring can later become a learned model while the safety gate stays deterministic.

## 2. Separate recommendation from permission

I did not want a single component to both choose and execute a money-related action. The agent proposes an action; the policy layer decides whether it is allowed, approval-gated, stopped or escalated.

This also makes it easier to answer a basic question during a review: "Why did this action happen?"

## 3. Use synthetic data on purpose

The dataset is generated from a fixed seed so anyone can recreate the same 250 rows. The goal is reproducibility, not realism at production scale. I avoided real payment/customer data because it is unnecessary for this prototype and introduces privacy risk.

## 4. Measure a batch, not one hand-picked example

The evaluation runs the same policy across the complete synthetic batch. I committed the output to `docs/evaluation.json` so the numbers in the README can be checked instead of being presentation-only claims.

## 5. What did not make the first version

I considered adding an LLM-generated sales message and a real Razorpay Test Mode payment flow. I left both out of the initial version because they would make the demo look larger without improving the core decision problem. The next integration I would add is Test Mode execution after an explicit approval step.

## Current limitations

- synthetic data is not evidence of production uplift;
- the current opportunity score is rule-based rather than learned from merchant history;
- there is no live merchant catalogue or CRM connection;
- the demo does not send messages or create real payment actions;
- policy thresholds would need merchant-specific calibration in production;
- a production system would require authentication, persistent storage, rate limiting and monitoring beyond this prototype.

## Validation checklist used for this version

- deterministic data generation;
- API request/response tests;
- safety-policy tests;
- approval-gate tests;
- stopping-rule tests;
- reproducible batch evaluation;
- CI workflow to rerun tests and evaluation.
