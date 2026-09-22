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

---

## DEC-RL-003 — Comparator code accepted for gated user Colab T4 execution

**Date:** 2026-09-21  
**Decision:** `CODE_ACCEPTED_FOR_USER_COLAB_RESEARCH`.

### Audited submission

- Claude implementation commit: `204f13e3f33edade7613fd9f84b2672569101e95`.
- PMO integration: PR #2, squash-merged to `main` as `a3d42a57718f921e2f5add9c3eead1e419cc4bc7`.
- Smoke suite: 16/16 checks passed; no research-scale result from the smoke package is promoted.

### Accepted implementation properties

- strict `SMOKE` versus `RESEARCH` namespaces and execution modes;
- RESEARCH fails closed without an NVIDIA T4 unless PMO explicitly authorizes a different CUDA GPU;
- two-holdout Base 4 TT reproduction gate is implemented before research training;
- frozen Base 4 TT rows are reused from the ledger rather than regenerated;
- empirical Merton calibration is training-slice only;
- checkpoint/resume and immutable attempt accounting are implemented;
- entropy time-scaling distinction between the frozen discrete objective and the continuous-time Merton-paper convention is explicit and unit-tested;
- no SESOI, superiority threshold or pure-jump interpretation is introduced.

### GPU qualification

The frozen Base 4 numerical contract is hybrid:

- tensor-heavy market simulation / block generation runs CUDA float32 batched on the T4;
- the frozen Base 3 learner rollout, critic fit and actor-gradient path remains vectorized NumPy float64 on CPU.

This is accepted for the current comparator because preserving the **same learner implementation** as the frozen SBJTS arm is scientifically more important than silently porting it to CUDA. A full CUDA learner port would create a new implementation lineage and requires its own numerical-equivalence protocol before paper use.

### User run authorization

The user may now execute `RUN_MODE="RESEARCH"` in the merged comparator notebook on paid Colab T4.

Hard gates remain binding: U0 source identity, U1 two-holdout reproduction, U2 calibration and U3 positive control must pass before U4 full training proceeds. A tolerance-only U1 pass is preserved and reported; a failed U1 blocks training.

### Historical development run

Commit `0bdd16b` and its research-scale outputs are retained only as `DEVELOPMENT_EVIDENCE`. They were executed before DEC-RL-002 and are not the active research evidence for the paper.

### Claim status

`CL-RL-006` remains **NOT_TESTED** until PMO audits the user's Colab research outputs. Code readiness does not promote a scientific claim.

---

## DEC-RL-004 — Direct Merton comparator accepted as scoped empirical paper evidence

**Date:** 2026-09-22  
**Decision:** `EMPIRICAL_EVIDENCE_ACCEPTED_WITH_SCOPE`; close the direct-comparator research question and move the project bottleneck to theory coupling.

### Research evidence accepted

The user Colab T4 run produced the intended research lineage:

- U0 source identity/fingerprint completed;
- U1 two-holdout Base 4 reproduction passed **bitwise exactly** on the 16 predeclared rows;
- U2 empirical Merton/GBM calibration passed using the frozen training slice only;
- U3 learner positive control passed;
- U4 trained 80/80 empirical-GBM RL policies with no seed replacement;
- U5 completed 24,000/24,000 Merton-on-SBJTS evaluations and reused the frozen 24,000 TT rows rather than retraining or re-evaluating the SBJTS arm;
- U6 analytic Merton remained secondary/descriptive;
- U7 produced the frozen crossed-cluster estimands.

### Primary scientific result

On the same frozen SBJTS target holdout:

- FULL: `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`;
- CAP50: `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`.

The frozen crossed-cluster 95% intervals exclude zero for all four contrasts.

PMO independently recomputed the contrasts from the raw TT and MT ledgers, obtaining 24,000 one-to-one matched pairs after removing the single previously known exact duplicate TT row. A stricter policy-level sensitivity analysis that collapses the 300 evaluation blocks within each training replication and bootstraps only the 40 paired policy units also leaves all four intervals away from zero, with the favorable sign in 40/40 replications for every endpoint/constraint stratum.

### Mechanism evidence retained

Average executed exposure is nearly identical across arms, so the gain is not primarily a leverage-level effect. Saved-policy analysis shows materially different state feedback:

- FULL lag-return response slope of executed mean action: about `-0.674` for SBJTS versus `+0.015` for Merton;
- FULL log-wealth response slope: about `-0.238` versus `-0.003`;
- CAP50 shows the same qualitative separation.

This supports the paper mechanism `training market law -> learned state feedback -> deployment outcome`, without claiming lagged return is the sole causal channel.

### Scope restrictions retained

- no universal superiority claim;
- no pure-jump causal claim;
- no external-market-validity claim from the current Base 2 ancestry;
- no retrospective conversion to confirmatory superiority;
- no claim that the four-feature learner observation is a complete Markov state;
- no claim that truncated Gaussian is globally optimal under SBJTS.

### Evidence preservation

The research outputs remain on Google Drive and are now pinned in GitHub by Drive file ID, byte size and SHA-256 in `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`. Compact mechanism/sensitivity evidence is also stored in the repository.

### Next research action

Open exactly one new executable ticket: `C-RLSBJTS-THEORY-COUPLING-01`.

The next deliverable is formal theory: wealth-law coupling, moment-matching non-equivalence, likelihood-ratio policy gradient under history dependence/partial observation, occupancy/continuation-value decomposition, theorem-to-code mapping, and cheap gate-mutation tests. No additional research-scale training is authorized at this stage.
