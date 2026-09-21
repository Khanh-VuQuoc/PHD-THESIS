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

The comparator distinguishes:

1. **RL–Merton / GBM-trained policy** — same learner class and budget, trained in a GBM calibrated from the frozen training slice;
2. **RL–SBJTS policy** — frozen Base 4 target-trained policy;
3. **analytic constrained Merton policy** — secondary benchmark, not a substitute for RL–Merton.

Primary question: when learned policies are evaluated on the same frozen SBJTS target holdout, does training in the richer SBJTS environment change terminal log wealth and CVaR log loss relative to training in a Merton/GBM environment?

---

## DEC-RL-002 — Claude is smoke-only; user owns Colab research execution

**Date:** 2026-09-21  
**Decision:** `PROCESS_CORRECTION`.

### Reason

Research-scale execution through Claude is an inefficient use of model usage and duplicates work that is better performed directly by the user on Google Colab/GPU. Claude's value is concentrated in derivation, scientific design, implementation, debugging, red-team review and production of a robust notebook.

### Binding execution rule

For RL–SBJTS from this decision onward:

```text
Claude = theory/design + implementation + static checks + SMOKE/PREFLIGHT only
User/Colab = real/frozen data + full training + full evaluation + research inference
GPT/PMO = code audit before the Colab run + scientific audit after the run
```

Claude must not run full replication grids, full real-data calibration, full holdout evaluations or expensive bootstrap/inference unless PMO and user explicitly override this rule.

### Required two-stage audit

1. **Code gate:** Claude returns `READY_FOR_PMO_CODE` after smoke only. PMO verifies design, fairness, checkpointing, output schema and resumability.
2. **Research gate:** after PMO approval, the user runs `RESEARCH` mode in Colab and publishes the generated evidence. PMO then audits the scientific results.

### Consequence for C-RLSBJTS-MERTON-COMP-01

The ticket is amended so Claude implements but does not execute the 80-policy / 24,000-evaluation research run. The notebook must cleanly separate `SMOKE` from `RESEARCH` and support restart without repeating completed units.

This decision governs subsequent computational tickets unless explicitly superseded.