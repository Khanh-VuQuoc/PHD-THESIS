# Expected RESEARCH outputs — C-RLSBJTS-MERTON-COMP-01

This directory is **empty by design**. It is filled by the user's Colab run on the
rented NVIDIA T4, not by Claude. Nothing under `../smoke/` may be moved here, and the
notebook refuses at runtime to write a SMOKE artifact into this namespace.

Evidence class of everything produced here: `USER_COLAB_RESEARCH_EVIDENCE`.

## How to produce these files

Open `notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb` in Colab, set
`Runtime > Change runtime type > T4 GPU`, set `RUN_MODE = "RESEARCH"` in the Step 00
cell, and run every cell from the top. The notebook stops immediately if CUDA is
unavailable or the allocated device is not a T4; there is no CPU fallback.

Stages run in order and each one is resumable. A disconnect is recovered by re-running
the notebook from the top with the same `MERTONCOMP_WORK` directory: completed units
are skipped, never repeated.

## Files this run must produce

| File | Stage | Contents | Gate |
|---|---|---|---|
| `hardware_manifest.json` | Step 00 | `torch.cuda.get_device_name(0)`, CUDA/cuDNN/PyTorch versions, VRAM, capability, `is_t4` | must show `cuda_available: true` and `is_t4: true` |
| `source_fingerprint.json` | U0 | SHA-256 of every frozen artifact consumed, recomputed protocol id, 17 Base 3 native AST component hashes, frozen environment fingerprint, training-slice digest | protocol id must equal `c9ef6548…`; any mismatch stops the run |
| `entropy_time_scaling_tests.json` | U0 | T1/T2/T3 for the discrete-vs-continuous entropy weighting, plus the empirical-curvature diagnostic | `ENTROPY_TIME_SCALING_TESTS_PASS` |
| `reproduction_check.json` | U1 | the predeclared 16-row two-holdout Base 4 TT reproduction, row by row, with bitwise and tolerance adjudication | `BASE4_TARGET_REPRODUCTION_PASS_EXACT` or `…_WITHIN_FROZEN_BACKEND_TOLERANCE`; anything else **stops the comparator** |
| `merton_calibration.json` | U2 | frozen-training-slice GBM calibration, its SHA-256, leakage controls, the predeclared Monte Carlo moment test | `MERTON_GBM_CALIBRATION_PASS` |
| `learner_positive_control.json` | U3 | PC1–PC5 on a bounded Merton-world run, against frozen `LEARNER_CONFIG` thresholds | `LEARNER_POSITIVE_CONTROL_PASS`, else stop before U4 |
| `training_attempts.csv` | U4 | one row per Merton training attempt, 80 expected, with seeds, status, failure type and policy SHA-256 | 0 seed replacements; failures stay in the denominator |
| `policies_merton.npz` | U4 | the 80 trained Merton actor weight matrices, keyed by immutable `attempt_id` | checkpointed after every replication |
| `evaluation_attempts.csv` | U5 | 24,000 expected `MERTON_MT` target-holdout attempts with endpoints and status | the `SBJTS_TT` arm must **not** appear: it is reused from the frozen ledger |
| `analytic_merton_results.csv` | U6 | 1,200 expected analytic rows: 2 constraints × 2 exploration conventions × 300 blocks | labelled `is_rl_trained: false` |
| `primary_estimands.json` | U7 | `Delta_W` and `Delta_CVaR` by stratum with crossed-bootstrap 95% intervals, secondary endpoints, analytic table, attempt accounting | records which frozen TT rows were joined and any that were missing |
| `resume_manifest.json` | U4/U5 | live progress and the exact resume unit | written after every evaluation block |

## Expected magnitudes, for sanity only

These are order-of-magnitude expectations from the frozen design, **not** predictions
of the result and **not** an acceptance criterion:

- 80 training attempts, 24,000 Merton evaluation attempts, 1,200 analytic attempts;
- 300 frozen evaluation blocks (20 holdout streams × 15 evaluation seeds), 600 paths
  per attempt, 60 engine steps per path;
- the frozen Base 4 target-holdout TT ledger supplies 24,000 rows that are **read**,
  never recomputed and never overwritten.

## What the run must never do

- retrain or overwrite the 80 frozen Base 4 SBJTS target policies;
- re-evaluate the SBJTS arm instead of reading the frozen ledger;
- replace a seed, drop a failed attempt, or impute a missing row;
- continue past a failed U1 reproduction gate;
- change `m`, the action bounds, the state, the wealth accounting, the budgets, the
  holdout namespace or any endpoint definition;
- introduce AMP, float16, bfloat16 or a non-CUDA fallback;
- introduce a SESOI or any superiority threshold after results are visible.

## After the run

Commit the files above into this directory and hand them to PMO. `CL-RL-006` stays
`NOT_TESTED` until PMO audits them. Smoke artifacts under `../smoke/` are never part of
that audit.
