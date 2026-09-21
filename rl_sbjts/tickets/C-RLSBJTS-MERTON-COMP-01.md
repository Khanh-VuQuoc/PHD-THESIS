# C-RLSBJTS-MERTON-COMP-01 — Direct RL–Merton comparator on frozen SBJTS holdout

**Status:** `READY_FOR_PMO_CODE`  
**Owner:** Claude — Technical Research Verifier / Implementation Lead  
**Research execution owner:** User / Google Colab  
**PMO:** GPT  
**Evidence target:** Claude delivers code-ready + smoke-passed; user later produces research evidence.

## 1. Single objective

Build a standalone, resumable GPU notebook that adds one scientifically fair **RL–Merton/GBM training-law arm** to the frozen RL–SBJTS study and is ready for the user to run in Colab against the **same frozen SBJTS target holdout**.

Claude's job is **design + implementation + smoke only**. Claude must not run the research-scale training/evaluation.

The eventual scientific comparison is between:

- frozen Base 4 SBJTS-target-trained policies; and
- newly trained Merton/GBM policies using the same RL learner, constraints, exploration setting and training budget.

The ticket asks a model-misspecification/training-environment question. It does **not** ask whether Merton is mathematically wrong inside a GBM world.

## 2. Source of truth

Read in this order:

1. `../00_CURRENT_STATE.md`
2. `../01_PMO_SKILL_RL_SBJTS.md`
3. `../04_CANONICAL_SOURCE_MAP.md`
4. `../02_CLAIM_LEDGER.md`
5. `../notebooks/frozen/05B_BASE4_SCIENTIFIC_EXPERIMENT_GPU_RESEARCH_v2_0_POINTER.md`
6. frozen Base 3 / snapshot / Base 4 release artifacts resolved at runtime.

Expected Base 4 protocol ID:

`c9ef65485a49d40356f3bbb02d491c4b73fcc9ebf0a22f02f64ab87e04a590d4`

Frozen market snapshot expected SHA-256:

`7e817762849118fc3abf8d4cf98ad8d65d921fa49cb0d1b3bb34d884b73c5b4a`

## 3. Hard execution ownership

### Claude may execute

- static source/code checks;
- synthetic/tiny unit tests;
- minimal end-to-end `SMOKE` mode;
- tiny checkpoint/resume test;
- tiny output-schema test.

### Claude must not execute

- full frozen/real-data calibration;
- research-scale Base 4 reproduction;
- the 40-replication-per-constraint Merton training grid;
- full target-holdout evaluation;
- full bootstrap/inference;
- any long GPU/CPU run whose purpose is to generate paper evidence.

If implementation reaches the point where real training/evaluation is needed, return `USER_COLAB_RUN_REQUIRED`.

## 4. Required notebook modes

The notebook must expose an explicit switch such as:

```python
RUN_MODE = "SMOKE"      # Claude may run
# RUN_MODE = "RESEARCH" # user runs in Colab after PMO code audit
```

### SMOKE namespace

- tiny/synthetic or minimally hydrated inputs only;
- tiny replications/path counts;
- separate output directory;
- cannot overwrite or be confused with research evidence;
- validates that the pipeline starts, trains minimally, evaluates minimally, writes artifacts and resumes.

### RESEARCH namespace

- uses frozen real sources;
- full budgets specified below;
- resumable/checkpointed;
- skips completed accepted units;
- never overwrites Base 4 frozen evidence;
- emits compact evidence files for GitHub/PMO audit.

## 5. Frozen scientific constraints for RESEARCH mode

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

## 6. Merton/GBM comparator definition

### 6.1 Main scientific comparator = empirical Merton/GBM

On the frozen training slice only, use the same equally weighted risky log increment consumed by the learner. Do not use target holdout statistics.

Let `dt` be the frozen time-step convention and `r_f` the Base 4 primary risk-free convention. In RESEARCH mode compute and freeze:

```text
m1 = mean(training risky log increment)
v1 = variance(training risky log increment)  # record ddof
sigma_M^2 = v1 / dt
mu_M - r_f = m1 / dt + 0.5 * sigma_M^2
```

No parameter search is allowed.

Claude must implement this function and test it on synthetic known data; the user performs the actual frozen-data calibration in Colab.

### 6.2 Secondary benchmark = analytic exploratory Merton policy

For each constraint stratum, compute the exploratory log-utility Merton policy implied by the same empirical `mu_M`, `sigma_M`, `r_f`, `m=0.01`, conditioned to the same hard interval.

This is secondary and must not replace learned RL–Merton.

## 7. Fairness contract

For eventual RL–Merton versus RL–SBJTS:

- same learner code and optimizer;
- same state representation;
- same action bounds;
- same `m`;
- same number of updates and paths/update;
- same replication count: 40 per constraint;
- pair replication index with frozen SBJTS target-training replication where possible;
- reuse learner-initialization/action-uniform seed schedule where structurally meaningful;
- no performance-based seed selection/replacement;
- failures remain in accounting;
- evaluate new Merton policies on the exact target holdout/evaluation namespace used by Base 4.

The Merton training environment differs by definition; do not fabricate common random numbers across incompatible generators.

## 8. Primary estimands

For each constraint stratum, with SBJTS target evaluation fixed:

```text
Delta_W = E[mean_terminal_log_wealth | train=SBJTS]
          - E[mean_terminal_log_wealth | train=MERTON_GBM]

Delta_CVaR = E[cvar_log_loss | train=SBJTS]
             - E[cvar_log_loss | train=MERTON_GBM]
```

- `Delta_W > 0` favours SBJTS training on wealth;
- `Delta_CVaR < 0` favours SBJTS training on CVaR loss.

RESEARCH mode must report two-sided 95% intervals using a paired/crossed bootstrap that respects replication x holdout x evaluation-seed structure. No superiority margin may be invented after results are seen.

## 9. Claude work queue — code + smoke only

### C0 — source interface and fingerprint code

Implement source resolution, protocol/hash checks and `source_fingerprint.json` writer. A static or tiny smoke validation is enough. Do not launch a research replay.

### C1 — Base 4 reproduction module

Implement deterministic reproduction code and comparison/tolerance logic for frozen target rows. In Claude smoke, test the mechanism on tiny/synthetic fixtures or the smallest harmless unit. The actual frozen-data reproduction gate is executed by the user in Colab.

### C2 — empirical GBM calibration module

Implement Section 6.1, with explicit units/ddof and a Monte Carlo tolerance calculator. Validate on synthetic known GBM data only or a tiny non-research fixture.

### C3 — Merton positive-control module

Implement analytic comparator and learner-recovery diagnostics. Claude may run a tiny toy/smoke training only. The frozen empirical positive-control run is reserved for user Colab.

### C4 — research training/evaluation implementation

Implement, but do not execute, the eventual research loops:

- `2 constraints x 40 replications = 80` Merton policies;
- `80 x 20 holdouts x 15 eval seeds = 24,000` learned-Merton target-evaluation attempts if all policies train;
- analytic Merton secondary evaluation;
- checkpoint/resume/attempt ledgers;
- primary estimand and bootstrap code.

### C5 — smoke end-to-end

Run the smallest end-to-end `SMOKE` configuration proving:

- notebook launches;
- a tiny Merton policy can train;
- a tiny evaluation completes;
- outputs have the expected schema;
- checkpoint/resume works;
- SMOKE artifacts are isolated from RESEARCH artifacts.

Then stop. Do not switch to RESEARCH mode.

## 10. User Colab research queue — after PMO code audit

The notebook must expose these ordered research stages so the user can run them without rewriting code:

### U0 — actual source fingerprint

Verify frozen protocol/snapshot/ancestry.

### U1 — actual Base 4 reproduction gate

Reproduce the predeclared frozen evaluation subset. If it fails, stop before Merton training.

### U2 — actual empirical Merton calibration

Calibrate from the frozen training slice only and freeze the calibration JSON.

### U3 — bounded empirical Merton positive control

Run the predeclared learner sanity check. If gross failure occurs, stop before the full comparator.

### U4 — full Merton training

Train 80 policies with checkpointing. No seed replacement.

### U5 — full target evaluation

Evaluate the Merton policies on the frozen SBJTS target holdout, up to 24,000 attempts, checkpointed/resumable.

### U6 — analytic Merton secondary evaluation

Run the two analytic constrained policies on the same target holdout.

### U7 — inference

Compute primary/secondary estimands, uncertainty, accounting and compact report.

## 11. Checkpoint policy

- Save after every completed training replication.
- Save evaluation after each `(constraint, replication, holdout)` block or more frequently.
- Never delete failed/partial attempts.
- No automatic seed replacement.
- Do not rerun a successful completed unit unless a documented reproducibility defect requires it.
- If Colab runtime is running out, stop cleanly and write `resume_manifest.json`.

## 12. Required files / edit allowlist

Claude may create/update only:

- `notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb`
- `reports/claude/RL_SBJTS_VS_MERTON_COMPARATOR_v1.md`
- `evidence/merton_comparator_v1/smoke/*`
- `evidence/merton_comparator_v1/research/README_EXPECTED_OUTPUTS.md`
- `evidence/merton_comparator_v1/resume_manifest.template.json`
- this ticket's `Status` / `Progress` section only.

Research output files are produced by the user's Colab run after PMO code approval.

Do not modify `00_CURRENT_STATE.md`, claim ledger, decision log, PMO skill, frozen notebook or frozen evidence.

## 13. Claude acceptance criteria

- **AC-C1 Design:** comparator implements the frozen fairness contract.
- **AC-C2 Separation:** `SMOKE` and `RESEARCH` are explicit and isolated.
- **AC-C3 Code path:** source fingerprint, reproduction, calibration, positive control, training, evaluation and inference stages are implemented.
- **AC-C4 Smoke:** tiny end-to-end execution passes.
- **AC-C5 Resumability:** checkpoint/resume is smoke-tested.
- **AC-C6 Accounting:** attempt ledgers preserve failures/partials.
- **AC-C7 Claim discipline:** smoke output is never reported as paper evidence.
- **AC-C8 Handoff:** exact one-pass Colab instructions and expected outputs are documented.

## 14. Stop conditions

Claude must stop and report rather than start a full run if:

- a required frozen interface cannot be resolved;
- implementation needs a change to frozen Base 4 mathematics/endpoints;
- smoke exposes a code defect requiring redesign;
- the next step would require real-data/full-grid/research-scale compute.

## 15. Claude completion response

Return:

```text
STATUS: READY_FOR_PMO_CODE or BLOCKED
FILES_CHANGED:
STATIC_TESTS:
SMOKE_TESTS / RESULTS:
COMMIT:
USER_COLAB_RUN_REQUIRED: YES
COLAB_RUN_INSTRUCTION:
EXPECTED_RESEARCH_OUTPUTS:
UNRESOLVED_ISSUES:
CLAIM_STATUS: NOT_TESTED — smoke only
```

Then set this ticket to `READY_FOR_PMO_CODE` and stop. PMO audits the implementation before the user spends Colab compute.

## Progress

- 2026-09-21 — PMO opened ticket.
- 2026-09-21 — PMO amended execution policy: Claude is restricted to design/code/smoke; all research-scale execution is reserved for user Colab.
- 2026-09-21 — Claude delivered design + code + smoke on branch `claude/eager-ride-091ooh`.
  Status `READY_FOR_PMO_CODE`. `USER_COLAB_RUN_REQUIRED: YES`. Detail in
  `../reports/claude/RL_SBJTS_VS_MERTON_COMPARATOR_v1.md`.

  - **Superseded run.** Commit `0bdd16b` on this branch executed the research-scale
    comparator before this execution policy existed. It is retained in git history as
    `DEVELOPMENT_EVIDENCE` only, its outputs have been removed from the working tree,
    and no number from it is carried forward.
  - **Mode separation.** `RUN_MODE` is `SMOKE` or `RESEARCH`, with separate output
    namespaces, separate budgets and separate evidence classes. The isolation is
    enforced at runtime: a smoke stage that tries to write under `research/` raises,
    and SMOKE is forced onto CPU even when a GPU is present.
  - **T4 hard requirement.** RESEARCH calls `require_research_hardware()` before any
    expensive stage: it raises without `torch.cuda.is_available()`, and raises again if
    the allocated device name does not contain `T4`. There is no CPU or NumPy fallback.
    `ALLOW_NON_T4` permits another CUDA device only with a written PMO authorisation,
    never CPU, and is recorded in `hardware_manifest.json`. `Context` re-asserts the
    `TORCH_CUDA_FLOAT32_BATCHED` contract after construction.
  - **Exact two-holdout reproduction gate.** The predeclared subset is fixed in code
    before any comparison runs: replications (0, 1) x both constraints x holdout streams
    (0, 1) x eval seeds (0, 1) = 16 TT rows. Bitwise equality is adjudicated first; the
    frozen Base 3 `GPU_EQ_ATOL`/`GPU_EQ_RTOL` is consulted only on failure and any use of
    it is recorded. A non-pass stops the comparator, and `stage_inference` independently
    refuses to join the frozen ledger without a passing gate.
  - **Frozen TT ledger reuse.** The SBJTS arm is no longer regenerated. `stage_evaluate`
    evaluates only the 80 Merton policies; the 24,000 SBJTS rows are read from the frozen
    Base 4 `evaluation_results_partial.csv` and joined on
    (stratum, replication, holdout, eval seed). Pairing holds by construction: both arms
    use the same frozen market seed and the same frozen evaluation action-uniform stream.
  - **Entropy time scaling documented and unit-tested.** The frozen Base 3 objective
    `E[log(W_T/W_0)] + m * sum_t H_t` and the Chau-Nguyen-Nguyen continuous-time objective
    `E[log W_T] + lambda * integral H_t dt` coincide on the frozen grid iff
    `m = lambda * dt`. With `dt = 1/250` the frozen `m = 0.01` is `lambda = 2.5`, and the
    paper's nominal `lambda = 0.01` is `m = 4e-5`: a factor of 250. Three tests pass
    non-vacuously (T1 sum identity exact to 4.4e-16; T2 grid invariance 2.0e-08 when `m`
    is rescaled against 0.131 when it is not; T3 separation 0.296), with every optimum
    strictly inside the frozen policy box. Nothing frozen is changed. The factor is
    common to both arms and cancels from `Delta`; it decides only which exploration
    weight the analytic benchmark is built at, so the comparator now reports the analytic
    Merton policy at both conventions, labelled.
  - **Smoke.** 16/16 checks pass in 19 s on CPU, including two negative tests that must
    fail closed: the RESEARCH hardware gate refuses without a T4, and inference refuses
    without a passing reproduction gate. Checkpoint/resume was proved by training 2 of 4
    tiny policies, re-entering, and training only the remaining 2.
  - **No research execution.** No frozen-data calibration at research scale, no 80-policy
    grid, no 24,000-attempt evaluation, no research bootstrap was run.
  - **Open for PMO.** (i) a CUDA port of the frozen NumPy float64 learner rollout is
    raised as `SCOPE CHANGE REQUEST — PMO DECISION REQUIRED` and was not made, since it is
    a numerical-equivalence question; (ii) `…_PASS_EXACT` is the expected U1 outcome on a
    T4, and a tolerance-only pass should be audited before U4 proceeds; (iii) which
    analytic exploration convention belongs in the paper.