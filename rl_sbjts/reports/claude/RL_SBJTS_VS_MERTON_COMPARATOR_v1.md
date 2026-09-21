# RL–SBJTS vs RL–Merton/GBM comparator — Claude code + smoke report v1

**Ticket:** `C-RLSBJTS-MERTON-COMP-01`  
**Status:** `READY_FOR_PMO_CODE` — design, implementation and smoke only.  
**Research execution owner:** user / Google Colab, paid NVIDIA T4.  
**Evidence class of everything in this report:** `SMOKE_EVIDENCE`. No comparator result is claimed or reported here.  
**Generated:** 2026-09-21T07:52:11.061005+00:00

---

## 0. What changed, and why

An earlier commit on this branch, `0bdd16b`, executed the full research-scale comparator before the current execution policy existed. Under DEC-RL-002 and the Colab T4 contract in `01_PMO_SKILL_RL_SBJTS.md` that run is **`DEVELOPMENT_EVIDENCE` only**. It is retained in git history, it is not carried forward as a research deliverable, and its output files have been removed from the working tree. Nothing in this report depends on its numbers.

The deliverable is now a standalone notebook with a hard `SMOKE` / `RESEARCH` split, plus the smoke evidence proving it runs, gates and resumes. Five things were changed on purpose relative to `0bdd16b`:

1. **RESEARCH hard-requires a CUDA NVIDIA T4**, with no CPU or NumPy fallback.
2. **The Base 4 reproduction gate is the predeclared two-holdout subset**, adjudicated bitwise first and only then against the frozen backend tolerance.
3. **The SBJTS arm is reused from the frozen Base 4 TT ledger**, not regenerated. `0bdd16b` regenerated it because the frozen ledger was not retrievable in that sandbox; in Colab it is, so regeneration is no longer justified.
4. **The entropy time-scaling distinction is documented and unit-tested.**
5. **Nothing research-scale was executed.** The smoke run is 19 seconds on CPU.

## 1. Mode and hardware separation

```python
RUN_MODE = "SMOKE"      # Claude may execute
RUN_MODE = "RESEARCH"   # user executes on the paid Colab T4
```

| | SMOKE | RESEARCH |
|---|---|---|
| Output namespace | `evidence/merton_comparator_v1/smoke/` | `evidence/merton_comparator_v1/research/` |
| Backend | `TORCH_CPU_FLOAT32_BATCHED`, CPU forced even if a GPU is present | `TORCH_CUDA_FLOAT32_BATCHED` on `cuda:0` |
| Hardware gate | none | `torch.cuda.is_available()` **and** the device name must contain `T4` |
| Budgets | 3 updates, 32 train paths, 2 replications, 1 holdout × 2 eval seeds | 400 updates, 512 train paths, 40 replications, 20 holdout × 15 eval seeds |
| Evidence class | `SMOKE_EVIDENCE`, `is_scientific_evidence: false` | `USER_COLAB_RESEARCH_EVIDENCE` |

The separation is enforced rather than documented. `assert_namespace_isolation` raises if a smoke stage tries to write under `research/`, `require_research_hardware` raises without a CUDA T4, and `Context.assert_backend_contract` re-checks the backend after construction. Two of the sixteen smoke checks exist purely to prove those two refusals actually fire; both do.

`ALLOW_NON_T4` exists so PMO can authorise a different CUDA device in writing. It cannot enable CPU, and the override plus its written reason are recorded in `hardware_manifest.json` for audit.

Evaluation `eval_paths` is held at the frozen 600 even in SMOKE. That is deliberate: it is the only way the smoke join against the frozen Base 4 TT ledger is dimensionally faithful. Smoke rows remain scientifically meaningless because training is 3 updates on 2 replications, and every artifact says so.

## 2. GPU research path

What RESEARCH sends to CUDA is the **market engine**: `simulate_three_channel_torch` runs float32 batched on `cuda:0`, which is exactly what frozen Base 4 did under `TORCH_CUDA_FLOAT32_BATCHED`. Market pairs are generated once per `(holdout, eval_seed)` block and held in memory while every policy is evaluated against them, so the 24,000 evaluations cost 300 engine runs rather than 24,000.

What stays on CPU, and why that is not a defect: the Base 3 learner rollout, critic fit and actor gradient are **frozen NumPy float64**. Base 4 ran them on CPU too. Porting them to CUDA would change the numerical contract the PMO skill says must be preserved first, so it is raised rather than done:

> `SCOPE CHANGE REQUEST — PMO DECISION REQUIRED`. A CUDA port of > `rollout_states_actions` would cut U5 wall-clock materially, since it is the > dominant cost at 24,000 rollouts. It is a numerical-equivalence question, not > a speed question: the rollout is float64 with a scipy truncated-normal inverse > CDF, and no float32 CUDA port can be assumed bit-identical. Claude has not > made that change. If PMO wants it, it needs its own equivalence protocol > against the frozen rows.

Within the frozen contract the notebook already avoids per-path Python loops (the rollout is vectorised over paths; only the 60 engine steps are sequential, which the frozen recursion requires), avoids GPU→CPU transfers inside the block loop, releases each market pair before the next, and checkpoints after every training replication and every evaluation block.

## 3. Entropy time scaling — the frozen discrete objective vs Chau–Nguyen–Nguyen

The continuous-time exploratory objective carries entropy as a **rate**, integrated over calendar time:

```text
J_cont(pi; lambda) = E[log W_T] + lambda * integral_0^T H(pi_t) dt
```

The frozen Base 3 objective, implemented in `soft_return_to_go` and consumed unchanged by Base 4, carries it **per decision**, summed over engine steps:

```text
J_disc(pi; m)      = E[log(W_T/W_0)] + m * sum_{t=0}^{N-1} H(pi_t)
```

Both use the same `H`, the differential entropy of the truncated-Gaussian action density on the hard interval. Discretising the integral on the frozen grid gives `integral H dt ≈ dt * sum_t H_t`, so the two coincide exactly iff

```text
m = lambda * dt        equivalently        lambda = m / dt
```

With the frozen `dt = 1/250`, the Base 4 primary setting `m = 0.01` is therefore **not** `lambda = 0.01`: it is `lambda = 2.5`. Conversely the paper's nominal `lambda = 0.01` corresponds to `m = 4e-05`. At equal nominal value the frozen learner weights exploration 250× more heavily.

### 3.1 What is and is not affected

Nothing frozen is changed. Both comparator arms optimise the same frozen discrete objective at the same `m`, so the factor is common to the arms and **cancels from `Delta`**. It decides exactly one thing: which exploration weight the analytic Merton benchmark must be built at. The comparator therefore evaluates the analytic policy at **both** conventions and labels them, because presenting only the paper-nominal one as an apples-to-apples empirical comparator is what the PMO red-team checklist forbids.

### 3.2 Unit tests

`smoke/entropy_time_scaling_tests.json` — **`ENTROPY_TIME_SCALING_TESTS_PASS`**. Optima are compared as the *executed* policy (location, scale), not as raw `(phi1, phi2)`, because the frozen parameterisation `scale^2 = exp(phi2) * m` is itself indexed by `m`. The search domain is the frozen policy box, which `phi2_box(m)` maps onto `[scale_floor, scale_ceiling]` for every `m`.

| Test | What it proves | LONG_ONLY_FULL | LONG_ONLY_CAP50 |
|---|---|---|---|
| T1 sum identity | `m·Σ H_t == (m/dt)·dt·Σ H_t` on the frozen entropy array, and `soft_return_to_go` reproduces the objective under its own `u > t` convention | 0.0e+00 / 4.4e-16 | 0.0e+00 / 1.1e-16 |
| T2 grid invariance | refining the grid by k while holding T fixed leaves the optimum unchanged **iff** m is rescaled to m/k, and that optimum equals the continuous one at `lambda = m/dt` | rescaled gap 2.0e-08, vs continuous 2.6e-08, **unrescaled 0.131** | rescaled 1.6e-08, vs continuous 2.6e-08, **unrescaled 0.131** |
| T3 scale separation | identifying `m` directly with `lambda` moves the optimum materially, so T2 is not passing vacuously | 0.296 | 0.296 |

The seven-orders-of-magnitude gap between the rescaled and unrescaled columns of T2 is the whole content of the test: `lambda` is grid-free, `m` is not. All optima visited are strictly inside the frozen policy box, so no result is a boundary artefact.

### 3.3 Empirical-curvature diagnostic, descriptive only

At the empirical calibration the per-step entropy term exceeds the per-step log-growth term by a factor of 110 (LONG_ONLY_CAP50) and 55 (LONG_ONLY_FULL). Consequently:

| Constraint | Exploration convention | effective λ | optimal executed scale | optimal latent location |
|---|---|---|---|---|
| LONG_ONLY_CAP50 | `frozen_discrete_m` | 2.5 | 7.6098 | 2.1181 |
| LONG_ONLY_CAP50 | `paper_nominal_lambda` | 0.01 | 0.4813 | 2.1182 |
| LONG_ONLY_FULL | `frozen_discrete_m` | 2.5 | 10.0000 (box edge) | 3.2936 |
| LONG_ONLY_FULL | `paper_nominal_lambda` | 0.01 | 0.4813 | 2.1182 |

The `paper_nominal_lambda` row reproduces the classical exploratory Merton policy exactly — location `(mu−r)/sigma^2` and scale `sqrt(m)/sigma` — which is an independent check that the analytic formula belongs to the continuous-time objective. The `frozen_discrete_m` row is the policy the frozen learner is actually pointed at. This is a property of the frozen objective, identical for both arms, and is neither changed nor corrected here.

## 4. Predeclared two-holdout Base 4 reproduction gate

The subset is fixed in `comparator_config.REPRODUCTION_SUBSET` before any comparison runs: replications [0, 1] × both constraints × holdout streams [0, 1] × eval seeds [0, 1] = **16 TT rows**. Two distinct holdout market streams and two distinct evaluation action seeds are what make the gate sensitive to a seed-namespace or market-generator defect rather than only to arithmetic drift.

Adjudication order: **bitwise equality first**; the frozen Base 3 `GPU_EQ_ATOL = 0.0002` / `GPU_EQ_RTOL = 2e-05` is consulted only if bitwise equality fails, and any use of it is recorded. No tolerance is chosen by this ticket. Outcomes:

- `BASE4_TARGET_REPRODUCTION_PASS_EXACT`
- `BASE4_TARGET_REPRODUCTION_PASS_WITHIN_FROZEN_BACKEND_TOLERANCE`
- `BLOCKED_REPRODUCTION_REFERENCE_ROWS_MISSING` / `…_ATTEMPT_ID_MISMATCH` / `BLOCKED_REPRODUCTION`

Anything that is not a `PASS` stops the comparator: the Merton arm is not trained and the frozen TT ledger is not joined. `stage_inference` re-checks the gate status and raises `INFERENCE_BLOCKED_BY_REPRODUCTION_GATE` independently, so the guard cannot be bypassed by running a stage out of order.

### What the smoke run shows

- The predeclared gate returned **`BLOCKED_REPRODUCTION_REFERENCE_ROWS_MISSING`**: 8/16 rows compared, 8 reference rows unavailable. That is the correct behaviour here and is the point — only the first 1 MiB of the 31 MB frozen ledger is retrievable in Claude's sandbox, so holdout stream 1 has no reference rows. **Claude cannot pass this gate, and does not pretend to.** U1 on Colab, with the full ledger, is the real gate.
- The gate *mechanism* was then exercised on the rows that do exist, via a SMOKE-only narrowing that is refused outright in RESEARCH mode and is stamped `is_predeclared_gate: false`. Result **`BASE4_TARGET_REPRODUCTION_PASS_WITHIN_FROZEN_BACKEND_TOLERANCE`** over 8 rows, all evaluation `attempt_id`s reproduced exactly, worst endpoint deviation 3.75e-08 against an `atol` of 0.0002.
- Bitwise equality was *not* reached in smoke, as expected: smoke runs the CPU float32 engine while Base 4 ran the CUDA float32 engine. On the user's T4 the backend matches Base 4 exactly, so `…_PASS_EXACT` is the expected U1 outcome and `…_WITHIN_FROZEN_BACKEND_TOLERANCE` would itself be worth reporting.

## 5. Reuse of the frozen TT ledger instead of regenerating the SBJTS arm

`stage_evaluate` evaluates **only** the new Merton policies. The SBJTS arm's 24,000 target-holdout rows are read from the frozen Base 4 `evaluation_results_partial.csv`, filtered to `cell_code == "TT"`, and joined in `stage_inference` on `(stratum, replication, holdout_env_stream, eval_seed)`. The frozen policies are never retrained and the frozen rows are never recomputed or overwritten.

Pairing survives the reuse by construction, not by assertion: both arms are evaluated at the same frozen market seed and the same frozen evaluation action-uniform stream, `rng_of("EVAL_ENV", action_seed % 2**31)`, drawn from the same frozen namespace. The reproduction gate is exactly what licenses treating a frozen row and a newly computed row as commensurable, which is why `stage_inference` refuses to run without it.

Smoke check: the evaluation ledger contains only the `MERTON_MT` arm, and inference reported `FROZEN_LEDGER_REUSE` with 8 frozen TT rows joined and 0 missing. Any row the frozen ledger cannot supply is listed in `rows_missing` rather than imputed.

## 6. Other stages, as implemented

**S0/U0 source fingerprint.** Verifies every consumed artifact by SHA-256, recomputes the protocol id from the 27 component registries in the 05A bundle, re-derives the 17 Base 3 native AST engine component hashes (0 mismatches) and checks the frozen training slice digest. Smoke confirmed the training slice matches `09811db465da1443…`.

**S2/U2 empirical GBM calibration.** Frozen training slice only (2110 daily rows, 2012-01-04 to 2020-05-22, EW log increment over the 4 snapshot assets), `dt = 1/250`, risk-free gross 1.0 per step, `ddof = 0`, all read from the frozen sources. Smoke result `MERTON_GBM_CALIBRATION_PASS`: `m1 = 0.000279427`, `v1 = 0.000172679`, `sigma_M = 0.207773`, `mu_M − r_f = 0.091442`. The predeclared 4-sigma Monte Carlo moment test on a disjoint seed namespace returned `z_mean = +0.413`, `z_var = -0.588`. No parameter search; zero validation or holdout rows read. This is a one-step mean/variance match, not a full-distribution match.

**S3/U3 positive control.** PC1–PC5 against frozen `LEARNER_CONFIG` thresholds. Smoke result `LEARNER_POSITIVE_CONTROL_PASS` on 4 tiny policies, with objective-ascent z between 215 and 481. The analytic reference shown alongside each policy is the one at `lambda = m/dt`, because that is the objective the learner actually optimises.

**S4/U4 training and S5/U5 evaluation.** Implemented at the frozen budgets, checkpointed after every replication and every block, resumable by immutable `attempt_id`. Failed attempts keep their ledger row and stay in the denominator; no seed is replaced. Smoke proved resume by training 2 of 4 policies, re-entering, and training only the remaining 2.

**S6/U6 analytic Merton.** Both exploration conventions, in its own table, labelled `is_rl_trained: false`.

**S7/U7 inference.** `crossed_bootstrap` and `stable_seed` are executed verbatim from the frozen Base 4 notebook rather than reimplemented. No SESOI, no hypothesis test, no superiority claim.

## 7. Smoke suite

`smoke/smoke_report.json` — **16/16 checks pass in 19.0 s on CPU.**

| # | Check | Result |
|---|---|---|
| 1 | `RESEARCH_HARDWARE_GATE_REFUSES_WITHOUT_T4` | PASS — RESEARCH_MODE_REQUIRES_CUDA |
| 2 | `SMOKE_CANNOT_WRITE_INTO_RESEARCH_NAMESPACE` | PASS — SMOKE_WRITE_INTO_RESEARCH_NAMESPACE_FORBIDDEN |
| 3 | `SMOKE_CONTEXT_BUILT` | PASS — backend=TORCH_CPU_FLOAT32_BATCHED device=cpu blocks=2 reps=[0, 1] |
| 4 | `S0_SOURCE_FINGERPRINT` | PASS — train_sha match, 17 AST components |
| 5 | `ENTROPY_TIME_SCALING_TESTS` | PASS — ENTROPY_TIME_SCALING_TESTS_PASS; lambda_equiv=2.5 |
| 6 | `S1_PREDECLARED_TWO_HOLDOUT_GATE_BLOCKS_ON_MISSING_REFERENCE` | PASS — BLOCKED_REPRODUCTION_REFERENCE_ROWS_MISSING; 8/16 rows, 8 reference rows unavailable locally |
| 7 | `S1_GATE_MECHANISM_PASSES_ON_AVAILABLE_ROWS` | PASS — BASE4_TARGET_REPRODUCTION_PASS_WITHIN_FROZEN_BACKEND_TOLERANCE; 8 rows; worst abs 3.75e-08 |
| 8 | `S2_MERTON_GBM_CALIBRATION` | PASS — MERTON_GBM_CALIBRATION_PASS; sigma_M=0.207773, z_mean=+0.41 |
| 9 | `S3_POSITIVE_CONTROL_GATES_EVALUATE` | PASS — LEARNER_POSITIVE_CONTROL_PASS; 4 policies, all_pass=True |
| 10 | `S4_TRAINING_PARTIAL` | PASS — 2 trained, 2/4 total |
| 11 | `S4_RESUME_SKIPS_COMPLETED_UNITS` | PASS — resumed and trained 2 of 4, none repeated |
| 12 | `S5_EVALUATION_AND_RESUME` | PASS — 8/8 Merton attempts over 2 blocks; resume visited 1 remaining block(s) |
| 13 | `S5_SBJTS_ARM_NOT_RE_EVALUATED` | PASS — evaluation ledger contains only the MERTON_MT arm |
| 14 | `OUTPUT_SCHEMAS` | PASS — training_attempts.csv:ok, evaluation_attempts.csv:ok, analytic_merton_results.csv:ok |
| 15 | `S7_INFERENCE_REUSES_FROZEN_TT_LEDGER` | PASS — 8 frozen TT rows joined, 0 missing, 20 estimands |
| 16 | `S7_REFUSES_WITHOUT_REPRODUCTION_GATE` | PASS — INFERENCE_BLOCKED_BY_REPRODUCTION_GATE |

Two of these are negative tests that must fail-closed and do: the RESEARCH hardware gate refuses on a machine without CUDA, and inference refuses when the reproduction gate has not passed.

## 8. Files

- `notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb` — the deliverable. Six modules are embedded as base64 and round-trip verified against the source that was actually smoke-executed, so the notebook cannot drift from the tested code.
- `evidence/merton_comparator_v1/smoke/` — smoke artifacts, all stamped `SMOKE_EVIDENCE`.
- `evidence/merton_comparator_v1/research/README_EXPECTED_OUTPUTS.md` — the file-by-file contract for the user's Colab run. The directory is otherwise empty by design.
- `evidence/merton_comparator_v1/resume_manifest.template.json` — the resume schema PMO should expect.

## 9. Unresolved issues for PMO

1. **CUDA port of the frozen learner rollout.** Raised in section 2 as a scope change. Not done. U5 wall-clock on the T4 depends on it.
2. **Expected U1 outcome.** On a T4 the backend matches Base 4, so `…_PASS_EXACT` is expected. If U1 returns `…_WITHIN_FROZEN_BACKEND_TOLERANCE` instead, that is a finding about CUDA determinism across driver or PyTorch versions and should be audited before U4 proceeds, even though the gate technically passes.
3. **Analytic benchmark convention.** The comparator reports both. If PMO wants only one in the paper, the `FROZEN_LEARNER_EQUIV` row is the like-for-like one; the `TICKET_NOMINAL_M` row is the paper's nominal setting and is not comparable to the learned arms without the disclosure in section 3.
4. **`0bdd16b`.** Superseded as a deliverable, retained as `DEVELOPMENT_EVIDENCE`. PMO may want it explicitly labelled in the decision log so it is never mistaken for a research run.

## 10. Claim status

- `CL-RL-006` (RL–SBJTS superior to RL–Merton/GBM) remains **`NOT_TESTED`**. Nothing in this report bears on it.
- `CL-RL-009` (a fair comparator is constructible) has code and smoke evidence only; PMO decides whether that is enough to move it off `PROSPECTIVE_DESIGN`.
- `CL-RL-007`, `CL-RL-010`, `CL-RL-011`, `CL-RL-012` are untouched and remain `BLOCKED`.
- Smoke artifacts are execution proofs. They are not comparator evidence and must never be reported as such.
