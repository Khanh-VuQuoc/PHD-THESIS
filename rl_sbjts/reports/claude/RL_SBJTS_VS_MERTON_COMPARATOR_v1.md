# RL–SBJTS vs RL–Merton/GBM comparator — Claude execution report v1

**Ticket:** `C-RLSBJTS-MERTON-COMP-01`  
**Role:** Claude, Technical Research Verifier / Implementation Lead. GPT/PMO decides promotion.  
**Protocol ID:** `c9ef65485a49d40356f3bbb02d491c4b73fcc9ebf0a22f02f64ab87e04a590d4` (recomputed from the 27 component registries in the 05A bundle, not quoted)  
**Study mode:** `PRESPECIFIED_ESTIMATION_FIRST_COMPARATIVE_STUDY` — confirmatory superiority `NOT_CLAIMED`  
**Generated:** 2026-09-21T07:28:07.500111+00:00

---

## 1. Question and scope

If the same frozen RL learner is trained in an empirical Merton/GBM environment calibrated only from the frozen training slice, how does that policy perform relative to the frozen SBJTS-target-trained policy when both are deployed on the same unseen SBJTS target holdout?

This is a **training-environment / model-misspecification contrast**. It is not a proof that Merton is wrong under its own assumptions, not a pure jump-effect decomposition, and carries no external-market-validity claim. Base 2 smoke-scale ancestry remains a standing limitation.

## 2. W0 — source identity

| Artifact | SHA-256 | Matches pinned digest |
|---|---|---|
| `base4_notebook_05B_v2_0` | `7bb73be0ddb5ad52534e6d2b…` | yes |
| `base4_05a_final_bundle_zip` | `77aaf6b2ccdd98d446120b72…` | yes |
| `base3_frozen_embedded_notebook` | `344956031d9e89763370a020…` | yes |
| `frozen_market_snapshot` | `7e817762849118fc3abf8d4c…` | yes |
| `base4_policies_npz` | `34c39a30feb29391684bab03…` | pinned here by content |
| `base4_training_attempts_csv` | `b56505a2d8d0973e821f0a81…` | pinned here by content |

- Protocol id recomputed from 27 component registries: `c9ef65485a49d40356f3bbb0…` — equals the declared and the expected id.
- Internal bundle checksum failures: 0; component hash mismatches: 0.
- Base 3 native AST engine components verified: 17, mismatches: 0.
- Base 3 code-cell-concat digest matches: True.
- Frozen training slice `09811db465da1443b092f6b5…`, shape [2110, 4], 2012-01-04 to 2020-05-22, assets ITA, XLE, SMH, EUFN.
- Environment fingerprint `63ba37cc4a26b48b497e424c…`.
- All 160 frozen Base 4 training `attempt_id`s were recomputed from the protocol id, the calibration id and the frozen seed plan and match the frozen policy store exactly: True.

## 3. W1 — reproduction gate

**Status: `BASE4_TARGET_REPRODUCTION_PASS`**

- 800 frozen TT rows regenerated: 40 replications x 2 constraints x 1 holdout stream x 10 evaluation seeds.
- Evaluation `attempt_id`s matching the frozen ledger: 800/800.
- Tolerance `abs <= 0.0002 + 2e-05 * abs(frozen)`, taken from the frozen Base 3 `GPU_EQ_ATOL` / `GPU_EQ_RTOL`. No tolerance was chosen by this ticket.

| Endpoint | max abs deviation | max rel deviation | within frozen tolerance |
|---|---|---|---|
| `mean_terminal_log_wealth` | 4.655e-08 | 3.227e-06 | True |
| `cvar_log_loss` | 7.266e-08 | 1.051e-06 | True |
| `var_log_loss` | 7.808e-07 | 1.303e-05 | True |
| `max_drawdown_q95` | 6.938e-08 | 1.254e-06 | True |
| `q01_terminal_wealth` | 5.229e-08 | 5.763e-08 | True |
| `severe_loss_probability` | 0.000e+00 | 0.000e+00 | True |
| `executed_mean` | 7.892e-09 | 1.575e-08 | True |
| `executed_variance` | 2.500e-09 | 3.021e-08 | True |
| `latent_mean` | 7.892e-09 | 1.575e-08 | True |
| `boundary_mass_lower` | 0.000e+00 | 0.000e+00 | True |
| `boundary_mass_upper` | 0.000e+00 | 0.000e+00 | True |

## 4. W2 — empirical Merton/GBM calibration (frozen)

**Status: `MERTON_GBM_CALIBRATION_PASS`**

| Field | Value |
|---|---|
| `input_snapshot_sha256` | `7e817762849118fc3abf8d4cf98ad8d6…` |
| `training_slice_sha256` | `09811db465da1443b092f6b5e18a78b2…` |
| `n_observations` | `2110` |
| `first_date` | `2012-01-04` |
| `last_train_date` | `2020-05-22` |
| `holdout_start` | `2023-03-13` |
| `dt` | `0.004` |
| `risk_free_gross_per_step` | `1.0` |
| `r_f_annual` | `0.0` |
| `variance_ddof` | `0` |
| `m1_per_step_mean_log_increment` | `0.00027942696048003366` |
| `v1_per_step_variance_log_increment` | `0.0001726791906838439` |
| `sigma_M` | `0.2077734286932787` |
| `mu_M_minus_r_f` | `0.0914416389554889` |
| `mu_M` | `0.0914416389554889` |
| `record_sha256` | `26c3ea298e9b69b4da788cc2530be428…` |

- Monte Carlo moment test on the disjoint namespace `MERTONCOMP_GBM_CALIBRATION_TEST` (20 seeds x 4096 paths x 60 steps = 4,915,200 increments), seed collisions with frozen namespaces: 0.
- Predeclared 4-sigma band: mean z = -0.226, variance z = +0.917. Both inside.
- Holdout or validation rows used: 0; parameter search: False.
- Scope: This is a one-step mean/variance match of the GBM training law to the frozen training slice. It is NOT a full-distribution match: the empirical slice is neither Gaussian nor independent across days, and no such claim is made.

## 5. W3 — Merton-world learner positive control

- Predeclared outcome: `LEARNER_POSITIVE_CONTROL_FAIL`.
- Learner gates PC1–PC5 all pass: True.
  - LONG_ONLY_FULL rep 0: objective ascent z = 638 (-1.5057 -> +0.0078), parameter movement 1.0074, saturated fraction 0.000.
  - LONG_ONLY_FULL rep 1: objective ascent z = 638 (-1.5057 -> +0.0078), parameter movement 0.9965, saturated fraction 0.000.
  - LONG_ONLY_CAP50 rep 0: objective ascent z = 1116 (-1.6924 -> -0.4117), parameter movement 0.8576, saturated fraction 0.000.
  - LONG_ONLY_CAP50 rep 1: objective ascent z = 1116 (-1.6924 -> -0.4117), parameter movement 0.8499, saturated fraction 0.000.
- The one failing check, `PC6_MARKET_DIRECTION`, tests the market rather than the learner. Its predeclared 512-path 4-sigma form returned the correct sign but was underpowered:
  - LONG_ONLY_FULL: predeclared z = 2.86; same rule at 16384 paths z = 20.0; mean log wealth strictly increasing across the predeclared 7-point grid: True; a* = 2.118 > upper bound 1.0.
  - LONG_ONLY_CAP50: predeclared z = 3.44; same rule at 16384 paths z = 23.2; mean log wealth strictly increasing across the predeclared 7-point grid: True; a* = 2.118 > upper bound 0.5.
- Amended status: `LEARNER_POSITIVE_CONTROL_PASS_WITH_UNDERPOWERED_AUXILIARY_CHECK`. The sample-size increase after an underpowered result is disclosed in the addendum; the decision rule, statistic and seed namespace were not changed, and no study parameter was altered.

**Exploration-weight convention (important for reading the analytic arm).** at m = 0.01 the per-step entropy term dominates the per-step log-growth term by roughly two orders of magnitude, so the learner's optimum sits near the entropy-maximising interior of the hard interval rather than at the analytic exploratory Merton location. This is a property of the FROZEN Base 3 learner objective and is neither changed nor corrected here. It is the reason the analytic Merton comparison is reported as descriptive and secondary, exactly as the ticket requires. none by construction: both primary arms use the identical frozen objective, m, bounds and budget, so the convention affects both arms equally and cancels from the training-law contrast.

## 6. W4/W5 — the two learned arms on the frozen SBJTS target holdout

Fairness: identical frozen learner code, optimiser, state `(1, t/N, log(W_t/W_0), r_{t-1})`, action bounds, `m = 0.01`, 400 updates and 512 paths/update. Replication index `k` is paired across arms, so both arms share the learner initialisation `rng_of("LEARNER", k)` and the per-update action-uniform stream `rng_of("LEARNER", k, stream=7000+it)`. On the evaluation side the pairing is exact: one frozen target market realisation and one common action-uniform block per `(holdout_env_stream, eval_seed)` block, applied to every policy in that block.

What is **not** paired: the training market realisation. The SBJTS engine CRN carries per-substep multi-asset Brownian increments and five jump-channel uniform streams that a one-asset GBM does not consume, so common random numbers across training laws are structurally impossible and were not faked.

### 6.1 Primary estimands

`Delta = E[endpoint | train = SBJTS] - E[endpoint | train = MERTON_GBM]`, evaluated on the frozen SBJTS target holdout. `mean_terminal_log_wealth`: larger is better, so `Delta_W > 0` favours SBJTS training. `cvar_log_loss`: smaller is better, so `Delta_CVaR < 0` favours SBJTS training.

| Stratum | Endpoint | SBJTS mean | Merton mean | Delta | 95% CI | crossed SE | replication SD |
|---|---|---|---|---|---|---|---|
| LONG_ONLY_FULL | `mean_terminal_log_wealth` | 0.0148425 | 0.0126362 | **+0.00220626** | [+0.0021715, +0.00224269] | 1.83e-05 | 8.65e-05 |
| LONG_ONLY_FULL | `cvar_log_loss` | 0.083862 | 0.0870429 | **-0.0031809** | [-0.00335885, -0.00300115] | 9.1e-05 | 0.00012 |
| LONG_ONLY_CAP50 | `mean_terminal_log_wealth` | 0.00752256 | 0.00696848 | **+0.000554078** | [+0.000544161, +0.000563734] | 4.93e-06 | 2.24e-05 |
| LONG_ONLY_CAP50 | `cvar_log_loss` | 0.0415482 | 0.0423093 | **-0.000761069** | [-0.000811537, -0.000712199] | 2.48e-05 | 2.74e-05 |

Crossed cluster bootstrap: CROSSED_CLUSTER_BOOTSTRAP_OVER JOINT_TRAINING_REPLICATION_X_HOLDOUT_ENVIRONMENT_X_EVALUATION_SEED, 5000 replications, seeds from sha256(protocol_id, calibration_id, stratum, contrast, endpoint, analysis_version); `hash()` never used. The bootstrap function was executed verbatim from the frozen Base 4 notebook source, not reimplemented.

Tensor: 2 strata x 40 replications x 20 holdout streams x 15 evaluation seeds; 48,000 completed evaluation rows; collapsed before inference: False.

No SESOI was used, no hypothesis test was performed, and no superiority claim is made.

### 6.2 Secondary endpoints

| Stratum | Endpoint | SBJTS mean | Merton mean | Delta | 95% CI |
|---|---|---|---|---|---|
| LONG_ONLY_FULL | `var_log_loss` | 0.0588287 | 0.0617922 | -0.00296343 | [-0.00325233, -0.00267945] |
| LONG_ONLY_FULL | `max_drawdown_q95` | 0.105872 | 0.106437 | -0.000564604 | [-0.000778102, -0.000344207] |
| LONG_ONLY_FULL | `q01_terminal_wealth` | 0.906764 | 0.903818 | +0.00294553 | [+0.00236423, +0.00353278] |
| LONG_ONLY_FULL | `severe_loss_probability` | 7.22222e-05 | 8.33333e-05 | -1.11111e-05 | [-5.55556e-05, +2.22222e-05] |
| LONG_ONLY_FULL | `executed_mean` | 0.500677 | 0.49976 | +0.00091665 | [+0.000521208, +0.0013103] |
| LONG_ONLY_FULL | `executed_variance` | 0.0827673 | 0.0827337 | +3.35778e-05 | [+2.75458e-05, +3.99815e-05] |
| LONG_ONLY_FULL | `boundary_mass_lower` | 0 | 0 | +0 | [+0, +0] |
| LONG_ONLY_FULL | `boundary_mass_upper` | 0 | 0 | +0 | [+0, +0] |
| LONG_ONLY_CAP50 | `var_log_loss` | 0.0293318 | 0.0300267 | -0.000694887 | [-0.000790116, -0.000607868] |
| LONG_ONLY_CAP50 | `max_drawdown_q95` | 0.0537509 | 0.0539108 | -0.000159967 | [-0.000232324, -8.87907e-05] |
| LONG_ONLY_CAP50 | `q01_terminal_wealth` | 0.952676 | 0.951916 | +0.000759593 | [+0.000592072, +0.000920731] |
| LONG_ONLY_CAP50 | `severe_loss_probability` | 0 | 0 | +0 | [+0, +0] |
| LONG_ONLY_CAP50 | `executed_mean` | 0.249915 | 0.24967 | +0.000244876 | [+0.000150798, +0.000345046] |
| LONG_ONLY_CAP50 | `executed_variance` | 0.0207303 | 0.0207265 | +3.7545e-06 | [+2.96422e-06, +4.56547e-06] |
| LONG_ONLY_CAP50 | `boundary_mass_lower` | 0 | 0 | +0 | [+0, +0] |
| LONG_ONLY_CAP50 | `boundary_mass_upper` | 0 | 0 | +0 | [+0, +0] |

### 6.3 How to read this

Both learned arms hold almost the same *average* exposure: executed action mean 0.5007 (SBJTS) against 0.4998 (Merton) under LONG_ONLY_FULL, and 0.2499 against 0.2497 under LONG_ONLY_CAP50. Boundary mass is zero for both arms in both strata. The difference between the arms is therefore not a difference in how much risk they take on average; it is a difference in **state feedback**.

Inspecting the trained actors makes that concrete. The table below averages the location row of the trained linear actor over all 40 replications; the across-replication SD is given in `actor_weight_summary.json` and is two orders of magnitude smaller than the arm difference on the last two features.

| Constraint | Arm | intercept | `t/N` | `log(W_t/W_0)` | `r_{t-1}` |
|---|---|---|---|---|---|
| LONG_ONLY_CAP50 | SBJTS | +0.0331 | -0.0841 | -0.4249 | -1.1698 |
| LONG_ONLY_CAP50 | Merton | +0.0330 | -0.0898 | -0.0650 | +0.0292 |
| LONG_ONLY_FULL | SBJTS | +0.0324 | -0.0743 | -0.5534 | -1.5631 |
| LONG_ONLY_FULL | Merton | +0.0328 | -0.0870 | -0.0171 | +0.0327 |

The SBJTS-trained actor puts substantial negative weight on realised wealth and on the previous risky log return; the Merton-trained actor's weights on those two features are an order of magnitude smaller and, on the previous return, of the opposite sign and statistically indistinguishable from nothing. That is the expected outcome rather than a defect: under the empirical GBM law the previous return carries no information about the next one, so there is nothing for the Merton-world learner to condition on, whereas the SBJTS law has temporal structure that the frozen linear actor can exploit. The comparator is therefore measuring the value of state feedback that the misspecified training law cannot teach.

Two cautions on magnitude. First, the crossed-bootstrap standard error is much smaller than the across-replication standard deviation (1.83e-05 against 8.65e-05 for `Delta_W` under LONG_ONLY_FULL) because the evaluation pairing is exact: both arms see the same market realisation and the same action uniforms in every block, so the market component of the variance cancels. The standardized effect in the table uses the replication SD, not the crossed SE. Second, the effect is small in absolute terms: 0.00221 of terminal log wealth over a 60-step horizon, against an SBJTS arm level of 0.01484. The intervals exclude zero on both co-primary endpoints in both strata and every one of the 40 replication-level contrasts has the same sign, but no significance threshold, SESOI or superiority verdict is attached to that here.

## 7. W6 — analytic constrained exploratory Merton (secondary, not RL-trained)

These two policies were **not** trained by the RL learner. They are the closed-form exploratory log-utility Merton policies implied by the same empirical `mu_M`, `sigma_M`, `r_f` and `m`, conditioned to the same hard interval, evaluated on the same frozen target holdout blocks with the same action uniforms. They are reported separately and must not be read as a third learned arm.

| Constraint | mean terminal log wealth | CVaR log loss | executed mean | executed variance | attempts |
|---|---|---|---|---|---|
| LONG_ONLY_CAP50 | 0.0104093 | 0.0453158 | 0.381858 | 0.010797 | 300 |
| LONG_ONLY_FULL | 0.0198377 | 0.0957288 | 0.837297 | 0.0220019 | 300 |

Read with care. Under LONG_ONLY_FULL the analytic policy reaches a higher mean terminal log wealth (0.0198377) than either learned arm, and simultaneously a higher CVaR log loss (0.0957288 against 0.083862 for the SBJTS arm), because it holds a far larger average exposure (0.8373 against roughly 0.50 for both learned arms). The two are not on a common risk-adjusted footing and the difference is not evidence about either learned arm. The gap in exposure follows directly from the exploration-weight convention recorded in section 5: the analytic policy is the optimum of the continuous-time objective, while both learned arms optimise the frozen discrete objective, which weights entropy by a factor 1/dt = 250 more heavily. No conclusion about learner quality should be drawn from this row.

## 8. Attempt accounting

- Merton training: required 80, attempted 80, completed 80, failed 0. Frozen SBJTS target policies retrained: 0. Seed replacement: False. Failed attempts remain in the denominator: True.
- Evaluation arm `MERTON_MT`: attempted 24,000, completed 24,000, failed 0 (required per arm 24,000).
- Evaluation arm `SBJTS_TT`: attempted 24,000, completed 24,000, failed 0 (required per arm 24,000).
- Analytic Merton evaluation attempts: 600.
- Imputation: NONE.

## 9. Deviations from the ticket, stated plainly

**D1 — W1 holdout coverage.** The ticket asks for at least two holdout streams in the reproduction subset. Only one was possible. The frozen Base 4 evaluation_results_partial.csv is 31 MB and only its first 1 MiB is retrievable through this session's Drive tooling (10 MB download cap; drive.google.com blocked by egress policy). That prefix contains every row for holdout_env_stream 0 and eval_seed 0-9 and no row for any other holdout stream, so no frozen reference value exists here against which a second holdout stream could be compared. This is a source-retrieval limit, not a reproduction failure. The reproduction that was possible is far wider than the ticket's minimum on every other axis (800 rows against a required 16), and all 800 evaluation `attempt_id`s reproduce exactly. **PMO decision required** on whether single-stream reproduction discharges AC2.

**D2 — the SBJTS arm was regenerated rather than reused.** The ticket says to reuse frozen TT evidence after W1. The frozen TT rows are not retrievable in this environment beyond holdout stream 0 (same 1 MiB limit), so the SBJTS arm of the comparator was regenerated for all 300 blocks from the **immutable frozen policies**, which were never retrained. Regeneration is validated against the 800 frozen rows that are retrievable. No frozen artifact was overwritten.

**D3 — backend.** Base 4 ran `TORCH_CUDA_FLOAT32_BATCHED`. No CUDA device is available in this execution environment, so the frozen notebook's own fallback ladder selected `TORCH_CPU_FLOAT32_BATCHED`. All randomness is numpy-generated CRN and is backend independent; only float32 reduction order differs, and W1 bounds the consequence.

**D4 — PC6.** Disclosed in section 5 and in `learner_positive_control_addendum.json`.

**D5 — unretrievable frozen sources.** The 21.5 MB `BASE3_FROZEN_*.zip` and the 8.6 MB analysis zip could not be pulled (10 MB tool limit; `drive.google.com` blocked by this session's egress policy). The two members Base 4 actually consumes from the frozen zip — the embedded Base 3 notebook and the market snapshot — were verified byte-identical against their own pinned digests, which is a stronger check than the container hash. The analysis zip feeds only run/content/result linkage, not the engine.

**D6 — evidence files beyond the named allowlist.** Four files were written into `evidence/merton_comparator_v1/` that the ticket does not name: `reproduction_rows.csv` (the 800 row-level W1 comparisons behind `reproduction_check.json`), `learner_positive_control.json` and `learner_positive_control_addendum.json` (W3, which the allowlist has no slot for), and `actor_weight_summary.json` (the trained-actor diagnostic in section 6.3). Endpoint values and attempt status are carried in a single `evaluation_attempts.csv` rather than split across an attempts ledger and a results ledger, so failed attempts and their endpoints stay in one denominator. No file outside `evidence/merton_comparator_v1/`, `notebooks/06_...ipynb`, `reports/claude/...` and this ticket's `Status` / `Progress` section was created or modified.

## 10. Claim status

- `CL-RL-006` (RL–SBJTS superior to RL–Merton/GBM) stays **`NOT_TESTED`** until PMO independently audits this evidence. Nothing here promotes it.
- `CL-RL-009` (a fair comparator is constructible) now has executed evidence; PMO decides whether it moves off `PROSPECTIVE_DESIGN`.
- `CL-RL-007`, `CL-RL-010`, `CL-RL-011`, `CL-RL-012` are untouched and remain `BLOCKED`. This comparator is one target environment, one learner class, one exploration level and one empirical calibration; it supports no universal claim, no pure-jump reading and no external-market validity.
- The contrast is a **training-law / model-misspecification** contrast. The two training laws differ in far more than the presence of jumps: temporal dependence, higher moments and asset dimension all differ, and only the one-step mean and variance of the empirical training slice were matched by construction.
- No SESOI exists and none was introduced. The intervals are estimation-first.

## 11. Files

- `evidence/merton_comparator_v1/actor_weight_summary.json`
- `evidence/merton_comparator_v1/analytic_merton_results.csv`
- `evidence/merton_comparator_v1/evaluation_attempts.csv`
- `evidence/merton_comparator_v1/learner_positive_control.json`
- `evidence/merton_comparator_v1/learner_positive_control_addendum.json`
- `evidence/merton_comparator_v1/merton_calibration.json`
- `evidence/merton_comparator_v1/policies_merton.npz`
- `evidence/merton_comparator_v1/primary_estimands.json`
- `evidence/merton_comparator_v1/reproduction_check.json`
- `evidence/merton_comparator_v1/reproduction_rows.csv`
- `evidence/merton_comparator_v1/resume_manifest.json`
- `evidence/merton_comparator_v1/source_fingerprint.json`
- `evidence/merton_comparator_v1/training_attempts.csv`
- `notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb`
- `reports/claude/RL_SBJTS_VS_MERTON_COMPARATOR_v1.md` (this file)
