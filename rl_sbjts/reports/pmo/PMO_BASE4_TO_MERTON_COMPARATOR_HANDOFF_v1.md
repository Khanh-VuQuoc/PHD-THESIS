# PMO handoff — Base 4 freeze -> RL–Merton comparator

**Date:** 2026-09-21  
**Decision:** Base 4 `ACCEPTED_WITH_QUALIFICATIONS` as frozen estimation-first evidence.  
**Successor:** `C-RLSBJTS-MERTON-COMP-01` only.

## Scope actually retained

Base 4 is not reopened. Its completed target-vs-affine-control comparison, attempt accounting, endpoint definitions, learner mathematics and target holdout namespace remain frozen.

The next scientific question is narrower and new:

> If the same RL learner is trained in an empirical Merton/GBM environment calibrated only from the frozen training slice, how does that policy perform relative to the frozen SBJTS-trained policy when both are deployed on the same unseen SBJTS target holdout?

This is a **training-environment/model-misspecification comparison**, not a proof that Merton is wrong under its own assumptions and not a pure-jump-effect decomposition.

## Base 4 findings carried forward

- Execution completed: 160/160 training attempts and 96,000/96,000 evaluation attempts.
- Existing target-training effect is estimation-first, not confirmatory superiority.
- Canonical one-step mean/variance matching passed for the Base 4 target/control pair, but terminal variance/path distribution remained unmatched.
- Temporal covariance/dependence accounts for the terminal variance residual at the decomposition level.
- Base 2 smoke-scale ancestry remains an external-validity limitation.

## Frozen comparison design for the successor

Primary learned arms:

1. frozen SBJTS-target-trained RL policies from Base 4;
2. new RL–Merton/GBM policies trained with the same learner, action bounds, `m=0.01`, training updates and paths/update.

Secondary benchmark:

3. analytic constrained exploratory Merton policy implied by the same empirical GBM calibration.

Evaluation environment for the scientific contrast: **the frozen SBJTS target holdout only**.

Primary endpoints remain:

- `mean_terminal_log_wealth`;
- `cvar_log_loss`.

FULL and CAP50 constraints are reported separately.

## PMO safeguards

Before any expensive Merton training, Claude must:

1. verify protocol / snapshot / frozen-source identities;
2. regenerate a subset of Base 4 target evaluations and reproduce frozen rows;
3. calibrate GBM from the frozen training slice only and freeze that calibration;
4. pass a bounded Merton-world learner sanity check.

Failure at any of these steps is a stop condition rather than a reason to improvise.

## Claim impact

The following remains `NOT_TESTED` until the ticket is executed and independently audited:

`RL–SBJTS > RL–Merton/GBM on the SBJTS target holdout.`

Even after a successful run, any conclusion must stay conditional on the tested frozen environment, learner, constraints and exploration level unless a future protocol broadens those dimensions.

## Claude instruction

Read `rl_sbjts/00_CURRENT_STATE.md` and execute only the sole `OPEN_FOR_CLAUDE` ticket. Use an isolated branch, preserve checkpointed partial evidence, set the ticket to `READY_FOR_PMO` when complete, then stop.
