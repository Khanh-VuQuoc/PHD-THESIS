# C-RLSBJTS-CONDLAW-DIAG-01 — Frozen conditional-law mechanism diagnostic

**Status:** `OPEN_FOR_CLAUDE`  
**Owner:** Claude — Technical Research Verifier / Implementation Lead  
**Research execution owner:** User / Google Colab if RESEARCH mode is needed  
**PMO:** GPT  
**Execution policy:** design + implementation + static/unit/smoke only for Claude; **no policy retraining and no research-scale execution by Claude**.

## 1. Scientific objective

Close the remaining mechanism gap without reopening training: directly characterize whether the frozen SBJTS target law contains lag-dependent conditional structure that is absent by construction from the empirical iid Merton/GBM comparator.

The diagnostic must connect the accepted theory result

\[
\mu_L(H_t)=E_L[r_t\mid H_t]
\]

and the accepted observed policy-response difference to the actual frozen simulator law, while remaining explicitly exploratory/descriptive.

Do **not** retrain RL policies. Do **not** claim causal attribution of the performance gain to lagged return alone.

## 2. Authoritative sources

Read in order:

1. `../00_CURRENT_STATE.md`
2. `../reports/pmo/PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`
3. `../reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
4. `../reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
5. frozen Base 3/Base 4 sources and comparator calibration pinned by `04_CANONICAL_SOURCE_MAP.md`.

## 3. Frozen laws

### SBJTS law

Use the accepted frozen SBJTS target market engine without changing calibration, bridge/jump logic, time step, horizon, or seed construction.

### Merton law

Use the accepted empirical Merton calibration already frozen by the comparator:

- `mu_M - r_f ≈ 0.0914416389554889`
- `sigma_M ≈ 0.2077734286932787`
- `dt = 1/250`

The Merton increment law is iid, so its theoretical conditional mean is constant.

## 4. Primary diagnostic

For generated market paths only, record pairs

\[
(r_{t-1},r_t)
\]

for all decision times after the first lag becomes available.

Standardize lagged returns using the accepted Merton one-step calibration:

\[
z_{t-1}=\frac{r_{t-1}-m_1}{\sqrt{v_1}}.
\]

Use one fixed common binning scheme for both laws:

```text
(-inf,-2], (-2,-1], (-1,-0.5], (-0.5,0],
(0,0.5], (0.5,1], (1,2], (2,inf)
```

For each law and bin report:

- number of observations;
- mean lagged return;
- `E[r_t | bin(z_{t-1})]`;
- deviation from the unconditional one-step mean;
- cluster-bootstrap 95% interval using independent simulation seed/block as the resampling unit.

The key visual is the conditional-mean response curve. Under Merton it should be flat up to Monte Carlo error; under SBJTS it may be state dependent.

## 5. Secondary diagnostics

Also report, by the same bins:

- conditional variance of `r_t`;
- left-tail probability `P(r_t <= q_0.05^M | bin)` where `q_0.05^M` is the fixed Merton 5% one-step quantile;
- a descriptive linear slope of `r_t` on `r_{t-1}` with seed-cluster uncertainty;
- lag-1 covariance/autocorrelation by law.

These are mechanism diagnostics, not new primary paper endpoints.

## 6. Policy overlay

Do not retrain or reevaluate policies. Reuse the saved policy-response evidence already in GitHub and create a compact overlay/table that juxtaposes:

1. the frozen conditional-mean curve; and
2. the previously accepted mean-action response to lagged return.

The purpose is to show whether the direction of learned policy feedback is qualitatively consistent with the conditional structure present in the frozen target law. Do not translate this into a causal share of the performance effect.

## 7. Research design / resource discipline

Claude must implement two modes:

### SMOKE

- synthetic or tiny frozen-engine fixture;
- enough paths to exercise all bins/schema where possible;
- CPU permitted;
- separate output namespace;
- run by Claude.

### RESEARCH

- frozen real environment;
- no RL actor/critic training;
- market simulation only;
- T4/CUDA if the frozen engine requires/benefits from it;
- resumable by simulation seed/block;
- user executes in Colab only after PMO code review.

Claude should propose a bounded seed/path budget sufficient for stable bin estimates and report an estimated runtime/memory footprint before PMO authorizes RESEARCH execution.

## 8. Required outputs

Claude may create/update only:

- `notebooks/07_RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1_0.ipynb`
- `reports/claude/RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1.md`
- `evidence/conditional_law_v1/smoke/*`
- `evidence/conditional_law_v1/research/README_EXPECTED_OUTPUTS.md`
- this ticket's Status / Progress section only.

Expected RESEARCH artifacts should include at minimum:

- `conditional_mean_bins.csv`
- `conditional_variance_bins.csv`
- `tail_probability_bins.csv`
- `law_summary.json`
- `simulation_attempts.csv`
- `hardware_manifest.json`
- `source_fingerprint.json`
- one manuscript-ready figure/table specification.

## 9. Hard claim restrictions

Do not claim:

- the lagged-return coordinate causes the full RL-SBJTS performance advantage;
- a pure jump effect is isolated;
- the conditional curve proves external market validity;
- a new confirmatory hypothesis test;
- universal superiority.

This diagnostic is post-hoc mechanism evidence supporting the already accepted domain-scoped comparator result.

## 10. Acceptance criteria

- exact frozen source/calibration fingerprinting;
- Merton iid control reproduces a flat conditional mean within Monte Carlo error in smoke/test fixtures;
- common bins and fixed definitions across laws;
- seed/block-level uncertainty, not row-iid uncertainty;
- no actor training;
- checkpoint/resume for research simulation blocks;
- clear output schema and one-pass Colab instructions;
- claim discipline preserved.

## 11. Claude completion response

Return:

```text
STATUS: READY_FOR_PMO_CODE or BLOCKED
FILES_CHANGED:
DESIGN:
STATIC/UNIT_TESTS:
SMOKE_RESULTS:
PROPOSED_RESEARCH_BUDGET:
ESTIMATED_COLAB_RUNTIME:
EXPECTED_OUTPUTS:
UNRESOLVED_ISSUES:
CLAIM_STATUS: EXPLORATORY_MECHANISM_ONLY
COMMIT:
```

Then mark `READY_FOR_PMO_CODE` and stop. Do not run RESEARCH mode.
