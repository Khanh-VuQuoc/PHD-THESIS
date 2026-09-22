# PMO Conditional-Law Diagnostic Code Acceptance v2

**Date:** 2026-09-22  
**Submission:** `c47304ceadc18fc73db087de15718a9a0abff0c3`  
**Ticket:** `C-RLSBJTS-CONDLAW-DIAG-01`  
**Verdict:** `CODE_ACCEPTED_FOR_USER_COLAB_RESEARCH`

## Decision

The targeted P1–P2 patch clears the two blocking findings from `PMO_CONDLAW_CODE_AUDIT_v1.md`. The diagnostic code is accepted for a bounded user-run RESEARCH execution on the paid Colab NVIDIA T4.

This authorization is for market simulation and conditional-law diagnostics only. It does **not** authorize policy retraining, actor/critic updates, lag-ablation retraining, or any new confirmatory performance claim.

## P1 — provenance correction accepted

Diagnostic artifacts now stamp their own lineage:

- `ticket = C-RLSBJTS-CONDLAW-DIAG-01`
- `producing_ticket = C-RLSBJTS-CONDLAW-DIAG-01`
- `diagnostic_id = C-RLSBJTS-CONDLAW-DIAG-01`
- `claim_status = EXPLORATORY_MECHANISM_ONLY`

The stale comparator producer ticket is no longer used for diagnostic outputs. Gate `S12_PRODUCER_TICKET_PROVENANCE` scans generated artifacts and includes a negative control proving that the old comparator stamping path is detected.

## P2 — dependency correction accepted

The RESEARCH path now stages only two content-pinned scientific inputs:

1. `03_RL_SBJTS_RESEARCH_GPU_HYBRID_v1_8.ipynb` with pinned SHA-256 `344956031d9e8976...` for the frozen market engine / AST verification;
2. `frozen_market_snapshot_U1_BASELINE_4.npz` with pinned SHA-256 `7e817762849118fc...` for the frozen calibration/environment inputs.

The diagnostic no longer stages `policies.npz`, `training_attempts.csv`, `evaluation_results_partial.csv`, `evaluation_results.csv`, or `BASE4_05A_FINAL_BUNDLE.zip`. The former filename/size ambiguity path is removed. The accepted compact policy-response tables are carried inline and verified by their pinned digests before use. Gate `S13_NO_RAW_LEDGER_DEPENDENCY` verifies the dependency contract statically and behaviorally.

## Verification retained

- 13/13 cheap static/unit/smoke checks pass;
- common fixed right-closed bins are unchanged;
- pairs `(r_{t-1}, r_t)` never cross path boundaries;
- Merton iid flatness positive control passes;
- AR(1) and pairing-destruction negative controls behave as intended;
- checkpoint/resume remains exact;
- uncertainty resamples simulation seed blocks rather than rows;
- seed namespaces are disjoint from frozen Base 4 seeds;
- AST gate confirms no actor/critic/learner-update path;
- RESEARCH remains T4/CUDA fail-closed;
- smoke values remain non-scientific execution evidence.

## Authorized research budget

The user may run notebook:

`rl_sbjts/notebooks/07_RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1_0.ipynb`

with:

- `RUN_MODE = "RESEARCH"`
- paid Colab NVIDIA T4
- backend `TORCH_CUDA_FLOAT32_BATCHED`
- `64` simulation blocks per law
- `3,072` paths per block
- `196,608` paths per law
- approximately `11,599,872` lagged pairs per law
- `4,000` block-bootstrap replications
- maximum practical session allowance: `45 minutes`

Checkpoint/resume should be left enabled. A partially completed run should be resumed, not restarted with replacement seeds.

## Required outputs for PMO result audit

At minimum retain the full `evidence/conditional_law_v1/research/` directory containing:

- `conditional_mean_bins.csv`
- `conditional_variance_bins.csv`
- `tail_probability_bins.csv`
- `law_summary.json`
- `simulation_attempts.csv`
- `hardware_manifest.json`
- `source_fingerprint.json`
- `policy_overlay.csv` / companion metadata if emitted
- `blocks/` checkpoints

The PMO research audit must first verify hardware/provenance, the Merton flatness control and complete block accounting before interpreting the SBJTS curve.

## Scientific interpretation allowed after a successful run

The diagnostic may support a statement that the frozen SBJTS law contains lag-dependent conditional structure absent from the iid empirical-Merton law, and that the sign of the saved policy response is qualitatively consistent with that structure.

It may **not** establish that lagged return causes the full RL–SBJTS performance advantage, isolate a pure jump effect, establish external validity, or convert the existing estimation-first comparator into a confirmatory superiority result.
