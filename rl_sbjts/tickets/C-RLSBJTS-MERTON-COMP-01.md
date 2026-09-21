# C-RLSBJTS-MERTON-COMP-01 — Direct RL–Merton comparator on frozen SBJTS holdout

**Status:** `OPEN_FOR_CLAUDE`  
**Owner:** Claude — Technical Research Verifier / Implementation Lead  
**PMO:** GPT  
**Evidence target:** development -> holdout estimation evidence; no confirmatory-superiority promotion.

## 1. Single objective

Build a standalone, resumable GPU notebook that adds one scientifically fair **RL–Merton/GBM training-law arm** to the frozen RL–SBJTS study and estimates, on the **same frozen SBJTS target holdout**, the difference between:

- frozen Base 4 SBJTS-target-trained policies; and
- newly trained Merton/GBM policies using the same RL learner, constraints, exploration setting and training budget.

The ticket asks a model-misspecification/training-environment question. It does **not** ask whether Merton is mathematically wrong inside a GBM world.

## 2. Source of truth

Read in this order:

1. `../00_CURRENT_STATE.md`
2. `../01_PMO_SKILL_RL_SBJTS.md`
3. `../04_CANONICAL_SOURCE_MAP.md`
4. `../02_CLAIM_LEDGER.md`
5. `../notebooks/frozen/05B_BASE4_SCIENTIFIC_EXPERIMENT_GPU_RESEARCH_v2_0_POINTER.md`, then retrieve and verify the actual frozen Drive notebook named there
6. frozen Base 3 / snapshot / Base 4 release artifacts loaded by the notebook at runtime.

Expected Base 4 protocol ID:

`c9ef65485a49d40356f3bbb02d491c4b73fcc9ebf0a22f02f64ab87e04a590d4`

Frozen market snapshot expected SHA-256:

`7e817762849118fc3abf8d4cf98ad8d65d921fa49cb0d1b3bb34d884b73c5b4a`

If these identities cannot be verified, stop.

## 3. Frozen scientific constraints

Do not modify or retune:

- SBJTS/Base 2 calibrated environment;
- Base 3 learner mathematics;
- state `(1, t/N, log(W_t/W_0), r_{t-1})`;
- wealth accounting;
- `m = 0.01`;
- LONG_ONLY_FULL and LONG_ONLY_CAP50 action bounds;
- actor/critic functional classes;
- 400 training updates;
- 512 paths/update;
- target holdout namespace: 20 holdout streams x 15 eval seeds;
- evaluation paths per attempt: 600;
- endpoint definitions;
- existing Base 4 policies/results.

No post-result SESOI may be introduced.

## 4. Merton/GBM comparator definition

### 4.1 Main scientific comparator = empirical Merton/GBM

Use the **same frozen training slice** and the same equally weighted risky log increment consumed by the learner. Do not use target holdout statistics.

Let `dt` be the frozen time-step convention and `r_f` the Base 4 primary risk-free convention. Compute and freeze:

```text
m1 = mean(training risky log increment)
v1 = variance(training risky log increment)  # explicitly record ddof
sigma_M^2 = v1 / dt
mu_M - r_f = m1 / dt + 0.5 * sigma_M^2
```

Generate GBM/Merton risky log increments under those frozen parameters.

Required calibration record:

- input snapshot SHA;
- exact training date/slice boundaries from the snapshot;
- number of observations;
- `dt`, `r_f`, `ddof`;
- `m1`, `v1`, `mu_M`, `sigma_M`;
- SHA-256 of the resulting calibration JSON.

No parameter search is allowed.

### 4.2 Secondary benchmark = analytic exploratory Merton policy

For each constraint stratum, compute the exploratory log-utility Merton policy implied by the same empirical `mu_M`, `sigma_M`, `r_f`, `m=0.01`, conditioned to the same hard interval.

This is a **secondary benchmark**. It must not replace the learned RL–Merton arm.

## 5. Fairness contract

For RL–Merton versus RL–SBJTS:

- same learner code and optimizer;
- same state representation;
- same action bounds;
- same `m`;
- same number of updates and paths/update;
- same replication count: 40 per constraint;
- pair the replication index with the frozen SBJTS target-training replication where possible;
- reuse the same learner-initialization/action-uniform seed schedule where structurally meaningful;
- do not select or replace seeds based on convergence/performance;
- failures remain in accounting;
- evaluate new Merton policies on the exact target holdout/evaluation seed namespace used by Base 4;
- regenerate evaluation randomness deterministically and prove reproducibility before the full run.

The Merton training environment may differ in its market innovation representation by definition; do not fake common random numbers across incompatible generators. Record exactly what is paired and what is not.

## 6. Primary estimands

For each stratum separately, with target SBJTS evaluation environment fixed:

```text
Delta_W = E[mean_terminal_log_wealth | train=SBJTS]
          - E[mean_terminal_log_wealth | train=MERTON_GBM]

Delta_CVaR = E[cvar_log_loss | train=SBJTS]
             - E[cvar_log_loss | train=MERTON_GBM]
```

Interpretation of signs:

- `Delta_W > 0` favours SBJTS training on wealth;
- `Delta_CVaR < 0` favours SBJTS training on CVaR loss.

Report two-sided 95% intervals using a paired/crossed bootstrap that respects replication x holdout x evaluation-seed structure. Do not invent a superiority margin.

### Secondary endpoints

Reuse the Base 4 endpoint set when available, including at least:

- q01 terminal wealth;
- max-drawdown q95;
- severe-loss probability;
- executed action mean/variance;
- boundary/saturation diagnostics.

Analytic Merton evaluation is descriptive/secondary.

## 7. Work queue

### W0 — hydrate and fingerprint sources

- Load frozen Base 4 notebook/release artifacts and Base 3 ancestry.
- Verify protocol ID, snapshot SHA and required frozen artifacts.
- Record hashes in `source_fingerprint.json`.

**Stop if identity fails.**

### W1 — reproduce frozen Base 4 evaluation before adding Merton

Using frozen SBJTS target policies, regenerate at least:

- 2 replication indices x
- 2 constraints x
- 2 holdout streams x
- 2 evaluation seeds

from the frozen target-evaluation namespace.

Compare recomputed endpoints against the existing Base 4 result rows. Prefer exact equality where deterministic; otherwise predeclare numeric tolerances before inspecting differences and justify backend effects.

Required status: `BASE4_TARGET_REPRODUCTION_PASS`.

**If this fails: stop with `BLOCKED_REPRODUCTION`. Do not train Merton.**

### W2 — freeze empirical GBM calibration

Implement Section 4.1. Run a Monte Carlo moment unit test on a disjoint calibration-test seed namespace. Predeclare tolerance from Monte Carlo standard error; do not tune parameters after the test.

Required status: `MERTON_GBM_CALIBRATION_PASS`.

### W3 — learner positive control

Before the expensive comparator, run a bounded Merton-world recovery check using the same learner and empirical GBM calibration. Compare learned executed policy summaries against the corresponding analytic exploratory Merton benchmark.

This gate is about gross implementation failure, not exact finite-sample equality. Predeclare thresholds from prior Base 1 logic or justify a new smoke tolerance before execution.

If the learner clearly fails the Merton-world check, stop before the research run.

### W4 — train only the new learned Merton arm

Train:

`2 constraints x 40 replications = 80 policies`

at the frozen research budget. Persist after every replication. Record immutable attempt IDs, seeds, status, failure type, final actor weights, and policy SHA-256.

Do **not** retrain the 80 frozen SBJTS target policies.

### W5 — evaluate Merton policies on the frozen SBJTS target holdout

For every new Merton policy, evaluate:

`20 holdout streams x 15 eval seeds`

with 600 paths/attempt, using the frozen Base 4 target holdout generator and deterministic seed schedule.

This implies 24,000 learned-Merton target-evaluation attempts if all 80 policies train successfully. Preserve failed-policy rows in the denominator/accounting.

Do not rerun all TT rows merely to generate duplicates. Reuse frozen TT evidence after W1 has established reproduction.

### W6 — analytic Merton secondary evaluation

Evaluate the two analytic constrained exploratory Merton policies on the same target holdout. Keep results in a separate table and clearly label that these policies were not RL-trained.

### W7 — inference and compact report

Produce primary estimates/intervals, secondary metrics, attempt accounting, and a claim-status block. Negative/parity results are fully acceptable.

## 8. Compute / checkpoint policy

- GPU notebook must be resumable after interruption.
- Save calibration, training and evaluation ledgers incrementally.
- Save policy/checkpoint material after every completed training replication.
- Save evaluation results after each `(constraint, replication, holdout)` block or more frequently.
- Never delete failed/partial attempts.
- No automatic seed replacement.
- No rerunning a completed successful unit unless a reproducibility defect is documented.
- If estimated remaining runtime exceeds the notebook's practical session budget, stop cleanly with a resume manifest rather than starting a unit likely to be lost.

## 9. Required files / edit allowlist

Claude may create/update only:

- `notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb`
- `reports/claude/RL_SBJTS_VS_MERTON_COMPARATOR_v1.md`
- `evidence/merton_comparator_v1/source_fingerprint.json`
- `evidence/merton_comparator_v1/merton_calibration.json`
- `evidence/merton_comparator_v1/reproduction_check.json`
- `evidence/merton_comparator_v1/training_attempts.csv`
- `evidence/merton_comparator_v1/policies_merton.npz` or a documented external artifact pointer if size blocks GitHub
- `evidence/merton_comparator_v1/evaluation_attempts.csv`
- `evidence/merton_comparator_v1/primary_estimands.json`
- `evidence/merton_comparator_v1/analytic_merton_results.csv`
- `evidence/merton_comparator_v1/resume_manifest.json`
- this ticket's `Status` / `Progress` section only.

Do not modify `00_CURRENT_STATE.md`, claim ledger, decision log, PMO skill, frozen notebook or frozen evidence.

## 10. Acceptance criteria

- **AC1 Source identity:** protocol/snapshot/frozen ancestry checks pass.
- **AC2 Reproduction:** required Base 4 target-evaluation subset reproduces before new training.
- **AC3 No leakage:** Merton calibration uses training slice only.
- **AC4 Calibration:** empirical GBM moment test passes under predeclared tolerance.
- **AC5 Learner sanity:** bounded Merton-world positive control passes or is transparently blocked before research execution.
- **AC6 Fairness:** same learner/constraints/`m`/budget and frozen target holdout.
- **AC7 Accounting:** all attempted, failed and partial units are retained; no silent seed replacement.
- **AC8 Resumability:** interrupted run can resume without repeating accepted units.
- **AC9 Estimands:** both primary endpoints reported separately by constraint with uncertainty.
- **AC10 Claim discipline:** no universal superiority, pure-jump effect, external market validation, or retrospective confirmatory claim.

## 11. Stop conditions

Stop and report rather than improvising if:

- frozen source identities fail;
- Base 4 evaluation reproduction fails;
- required snapshot/Base 3/Base 4 policy artifact cannot be resolved;
- empirical Merton calibration accidentally touches holdout data;
- learner positive control has a clear implementation failure;
- a requested change would alter frozen Base 4 mathematics or endpoint definitions;
- a full run would require seed replacement or hidden dropping of failures.

## 12. Completion response

Return:

```text
STATUS:
FILES_CHANGED:
TESTS_RUN / RESULTS:
COMMIT:
PRIMARY_RESULT:
ATTEMPT_ACCOUNTING:
UNRESOLVED_ISSUES:
CLAIM_STATUS:
RESUME_ACTION_IF_PARTIAL:
```

Then set this ticket to `READY_FOR_PMO` and stop. PMO decides whether any claim is promoted.

## Progress

- 2026-09-21 — PMO opened ticket. No comparator result exists yet.
