# RL–SBJTS theory supersession note v1

**Date:** 2026-09-28  
**Scope:** editorial / theory-consistency only. No experiment, retraining, estimand, claim or frozen evidence is changed by this note.  
**Applies to:** `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md` (accepted submission `ed7e9b5…` under `PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`).

The accepted theory report is left unedited so that its provenance stays intact. Where its historical text conflicts with the final accepted state, this note governs. None of the items below may be copied into the manuscript in their superseded form.

## A. Old P3 wording on A4 is superseded

The P3 row of the report's patch-response table says that (A4) was "reduced to first-moment integrability of terminal log wealth", i.e. `E|X_N - X_0| < infinity`. That reduction presumed a uniformly bounded actor-weight score. It was withdrawn by P6 (`PMO_THEORY_COUPLING_PATCH_AUDIT_v2.md`) and **must not be used**, because the actor-weight score chains through the unbounded state `S_t`.

## B. Authoritative regularity statement

The authoritative T3 regularity statement is:

- **(A4)** a general domination / integrability assumption on the score-weighted soft return and the direct entropy derivative, over a neighbourhood `U` of `theta_0`; and
- **(A4-mixed)** the assumed sufficient condition

  `sup_{theta in U} E[ (1 + max_{t<=N} ||S_t||) (1 + |R_soft_theta(tau)|) ] < infinity`.

Both are **assumptions on the training law**. Neither is proved for the frozen SBJTS law, and the T3 policy-gradient theorem is stated conditionally on them.

## C. Conditional-law diagnostic is no longer pending

The report's "Unresolved theory issues for PMO", item 2, says the conditional-law diagnostic is "specified but not executed" and carries a `SCOPE CHANGE REQUEST`. That is superseded. The diagnostic `C-RLSBJTS-CONDLAW-DIAG-01` was run on the authorized user-Colab T4 budget (64 × 3,072 paths per law, 4,000 block-bootstrap replicates) and accepted as exploratory mechanism evidence under `PMO_CONDLAW_RESULT_AUDIT_v1.md`.

## D. Lag-ablation retraining

The lag-ablation retraining contrast named in the same item remains **NOT AUTHORIZED**. `STOP EXPERIMENTS` remains binding.

## E. Two different lag quantities

These are different mathematical objects and **must never be quoted interchangeably**:

| quantity | approx. value (SBJTS) | source | what it is |
|---|---:|---|---|
| raw actor-weight lag coefficient | `-1.56` | theory report §T2b | the entry of the linear actor weight on the `r_{t-1}` feature, *before* the bounded raw-to-policy transform and truncation |
| executed-policy local lag-response slope | `-0.674` (LONG_ONLY_FULL) | DEC-RL-004 / saved-policy mechanism evidence | the slope of the executed mean action with respect to lagged return, *after* the transform and truncation |

The Merton counterparts (about `+0.03` raw vs about `+0.015` executed slope) follow the same distinction.
