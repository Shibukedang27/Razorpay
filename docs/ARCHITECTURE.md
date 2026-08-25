# Architecture

```mermaid
flowchart TD
M[Merchant / Demo UI] --> API[FastAPI API]
API --> S[Signal Normalizer]
S --> A[Growth Decision Agent]
A --> P[Deterministic Policy & Gating Engine]
P -->|allowed| X[Action Executor / Test-mode Adapter]
P -->|sensitive| H[Human Approval]
X --> V[Outcome Verifier]
H --> V
V --> L[Append-only Audit Trail]
V --> K[Metrics & Evaluation]
```

AI-style reasoning is intentionally separated from financial execution. Sensitive incentives are bounded and require approval. Stopping rules prevent repeated contact on stale carts.
