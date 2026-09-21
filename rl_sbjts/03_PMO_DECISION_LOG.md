# 03_PMO_DECISION_LOG — RL–SBJTS

## DEC-RL-001 — Freeze Base 4 and open direct Merton comparator

**Date:** 2026-09-21  
**Decision:** `ACCEPTED_WITH_QUALIFICATIONS` for Base 4 as estimation-first evidence; open one bounded comparator extension.

### Retained findings

- Base 4 completed its frozen execution cleanly.
- The target-SBJTS training law differs from the affine-calibrated no-jump control in target-holdout wealth/tail outcomes.
- One-step canonical mean/variance matching does not remove terminal/path differences.
- F-032 supports a temporal-dependence/cross-time covariance explanation for the residual terminal-variance gap.

### Claim restrictions retained

- No pure-jump-effect claim.
- No full-distribution-match claim.
- No confirmatory-superiority claim without prospective SESOI.
- No external-market-validity claim from smoke-scale Base 2 ancestry.
- No RL–SBJTS > RL–Merton claim because Merton has not yet been a direct training-law comparator.

### New research action

Open exactly one executable ticket: `C-RLSBJTS-MERTON-COMP-01`.

The comparator must distinguish:

1. **RL–Merton / GBM-trained policy** — same learner class and budget, trained in a GBM calibrated from the frozen training slice;
2. **RL–SBJTS policy** — frozen Base 4 target-trained policy;
3. **analytic constrained Merton policy** — optional secondary benchmark, not a substitute for RL–Merton.

Primary question: when all learned policies are evaluated on the same frozen SBJTS target holdout, does training in the richer SBJTS environment change terminal log wealth and CVaR log loss relative to training in a Merton/GBM environment?

### Why this successor was chosen

This directly extends the original exploratory-Merton paper and answers a more interpretable model-misspecification question than adding another internal SBJTS ablation. It also reuses frozen Base 4 target policies/holdout infrastructure instead of rerunning already accepted work.
