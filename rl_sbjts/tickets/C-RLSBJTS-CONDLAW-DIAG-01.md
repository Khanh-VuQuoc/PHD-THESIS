# C-RLSBJTS-CONDLAW-DIAG-01 — Frozen conditional-law mechanism diagnostic

**Status:** `READY_FOR_PMO_CODE`  
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

## 12. Progress

### 2026-09-22 — Claude — `READY_FOR_PMO_CODE`

Design, implementation and smoke only. **No policy was trained or evaluated, and
RESEARCH mode was not run** — it hard-requires a CUDA NVIDIA T4 and this sandbox has no
GPU. 11/11 smoke checks pass in 6.2 s on CPU, four of them controls that must fail or
block and do. PMO state, decision log, claim ledger and all frozen/comparator evidence
untouched; `main` synced before work.

Delivered against the section 8 allowlist:

- `notebooks/07_RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1_0.ipynb` (26 cells; the eight
  modules plus the namespace loader are carried as base64 and round-trip verified
  byte-for-byte against what was smoke-executed)
- `reports/claude/RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1.md`
- `evidence/conditional_law_v1/smoke/*` (schema, checks, 12 block checkpoints)
- `evidence/conditional_law_v1/research/README_EXPECTED_OUTPUTS.md`

**Design.** Pairs `(r_{t-1}, r_t)` for every decision time after the first lag,
never across a path boundary; lagged returns standardised with the frozen Merton
one-step calibration and the same fixed right-closed bins applied to both laws. Every
reported quantity is a function of per-(law, block, bin) sufficient statistics, which is
what makes the run resumable at block granularity, makes a resumed run bit-exact against
an uninterrupted one, and makes the cluster bootstrap cheap. The resampling unit is the
simulation seed block, as section 10 requires.

**A method correction worth PMO's attention.** My first flatness control read eight
per-bin 95% intervals and required all to cover `m1`. That is a multiplicity error and it
duly failed on honest iid data: with eight bins at least one miss has probability about
1 - 0.95^8 = 34% under a perfectly flat law. Bonferroni fixes the level but needs a 0.3%
bootstrap percentile, which a few dozen blocks cannot resolve. The package now uses a
simultaneous studentized sup-statistic over bins, which asks the simultaneous question
directly and needs only a central percentile. Merton returns sup 1.057 against a critical
value of 2.696 (flat); a mild injected AR(1) at rho=0.15 returns 42.563 against 2.710 and
a slope interval [0.1456, 0.1524] excluding zero. The gate that passes on iid data fails
decisively on dependence.

**Controls.** Merton flatness (positive control, and the notebook raises in BOTH modes if
it fails); AR(1) injection (negative); pairing destruction — permuting each step's column
preserves every one-step marginal exactly while removing the time linkage, moving the
SBJTS fixture slope from -0.1335 to -0.0093, so a surviving slope could not have been a
marginal artefact; resume exactness; cluster unit (block interval 1.35x the row-iid
width, single-block case refused); AST gate proving no actor, critic or learner-update
symbol is referenced anywhere on the diagnostic path; numeric seed isolation (128
diagnostic seeds against 720 Base 4 training/holdout seeds, empty intersection);
namespace isolation both directions; and the T4 requirement refusing to run here.

**Smoke numbers are not evidence.** The fixture is 6 blocks x 64 paths per law. It exists
to exercise every bin and the whole schema, and all eight bins populate for both laws. I
have deliberately drawn no inference from its SBJTS slope, and any quotation of it as a
finding should be treated as an error.

**Proposed bounded RESEARCH budget:** 64 blocks x 3,072 paths per law = 196,608 paths and
11,599,872 lagged pairs per law, 4,000 bootstrap replicates, on the paid Colab T4 under
`TORCH_CUDA_FLOAT32_BATCHED`. Blocks are favoured over paths-per-block because
uncertainty is quantified at the block level. Sizing: the tail bins hold about 2% of
pairs, giving a row-level standard error near 3.4e-05 and about 4.6e-05 after the measured
1.35x block inflation — fine enough for conditional-mean deviations of order 1e-4.
Estimated 11 minutes of SBJTS simulation from a two-point fit of the frozen engine
(marginal about 3.4 ms per path), seconds for Merton, a few minutes for the bootstrap;
**requesting a 45-minute allowance**, peak memory about 0.9 GB.

Honest limitation on that estimate: it is a CPU measurement, since Claude has no GPU
here, so the CUDA path is untimed and the allowance is deliberately loose. A first
timing in this session came out 40x more expensive per path and was pure torch warm-up,
which is why the reported figures come from a two-point fit after warm-up rather than a
single measurement. The T4 requirement itself is scientific rather than performance
driven: the accepted comparator lineage ran the frozen engine under
`TORCH_CUDA_FLOAT32_BATCHED`, and characterising the same law under a different numerical
backend would not be the same measurement.

**Claim discipline preserved.** `EXPLORATORY_MECHANISM_ONLY` throughout. No causal
attribution of the performance gain to the lagged-return channel, no pure-jump isolation,
no external-validity claim, no confirmatory test, no universal superiority. The policy
overlay is read-only and direction-only: it compares the SIGN of the already-accepted
learned action response with the sign of the law's own conditional structure, and carries
no magnitude and no share of the performance gap.
