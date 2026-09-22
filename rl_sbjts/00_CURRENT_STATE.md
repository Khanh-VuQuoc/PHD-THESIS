# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **THEORY_ACCEPTED / CONDLAW_USER_COLAB_RESEARCH_AUTHORIZED** — direct comparator and T1–T5 theory backbone are accepted. Conditional-law diagnostic code has passed PMO re-audit and is authorized for one bounded user-run RESEARCH execution. |
| Sole executable ticket | `tickets/C-RLSBJTS-CONDLAW-DIAG-01.md` — code accepted; next action is user Colab T4 RESEARCH run, not Claude execution. |
| Closed theory ticket | `tickets/C-RLSBJTS-THEORY-COUPLING-01.md` — final submission `ed7e9b5a15bdc1c52c309fc6b3165943fe225ed8` accepted by PMO. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Mechanism evidence | Average executed exposure is nearly unchanged, while saved SBJTS actors show strong negative lag-return and wealth-state feedback and Merton actors are nearly flat. FULL lag-response slope ≈ `-0.674` for SBJTS vs `+0.015` for Merton. |
| Theory status | **ACCEPTED_WITH_STATED_ASSUMPTIONS.** T1 exact wealth coupling; T2 moment/path-law non-equivalence; T3 history-state likelihood-ratio gradient without assuming the four-feature observation is Markov; T4 symmetric occupancy/continuation-value decomposition; T5 structural lagged-return mechanism; entropy scaling `m=lambda*dt`. |
| T3 regularity | The theorem is conditional on A4, or the sufficient mixed condition `sup_theta E[(1+max_t||S_t||)(1+|R_soft|)] < infinity`; this is assumed, not claimed verified for the frozen SBJTS law. |
| Conditional-law code audit | Submission `c47304ceadc18fc73db087de15718a9a0abff0c3` is **CODE_ACCEPTED_FOR_USER_COLAB_RESEARCH**. P1 provenance and P2 dependency findings are closed. 13/13 cheap checks pass. |
| Authorized diagnostic budget | `64 blocks × 3,072 paths per law`, `4,000` block-bootstrap replicates, `TORCH_CUDA_FLOAT32_BATCHED` on paid Colab NVIDIA T4, up to 45 minutes. Checkpoint/resume required; no replacement seeds. |
| Diagnostic code acceptance note | `reports/pmo/PMO_CONDLAW_CODE_ACCEPTANCE_v2.md`. |
| Required result audit | Before interpreting the SBJTS curve, verify T4 hardware/provenance, complete block accounting, source fingerprints, and the Merton iid flatness control. |
| Evidence location | Comparator research outputs remain on Drive under `merton_comparator_v1/evidence/research/`; the conditional-law run should retain its full `evidence/conditional_law_v1/research/` directory for PMO audit. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim, no claim that lagged return alone causes the observed gain. |
| Next PMO decision | Audit the user's conditional-law RESEARCH outputs. If the run is complete and the Merton control passes, decide whether the mechanism figure/table is manuscript-ready and then stop experiments / integrate the paper. |

## Current scientific narrative

The paper is organized around

\[
\boxed{
\text{training market law}
\rightarrow
\text{conditional/path structure}
\rightarrow
\text{RL state occupancy and continuation values}
\rightarrow
\text{learned feedback policy}
\rightarrow
\text{wealth and tail-risk outcomes}
}.
\]

The scientific backbone is already in place:

1. **Path-law evidence:** Base 4 shows that matching local canonical mean/variance does not match terminal/path behavior.
2. **Direct performance evidence:** RL–SBJTS outperforms matched RL–Merton/GBM on the frozen SBJTS deployment law in wealth and CVaR loss under both frozen constraints.
3. **Mechanism evidence:** the gain is not explained by average risky exposure; the saved policies encode materially different feedback to lagged return and current wealth.
4. **Theory:** T1–T5 formally connect the market law to wealth increments, policy gradients, state occupancy, continuation values and lagged-return information, with regularity assumptions stated explicitly.

The remaining empirical mechanism task is intentionally narrow: characterize the frozen conditional return law directly. No policy retraining is authorized.

## User Colab run now authorized

Run:

`rl_sbjts/notebooks/07_RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1_0.ipynb`

with:

```text
RUN_MODE = "RESEARCH"
GPU = NVIDIA T4
backend = TORCH_CUDA_FLOAT32_BATCHED
blocks_per_law = 64
paths_per_block = 3072
bootstrap_replicates = 4000
```

This run is market simulation only. It must not construct/train/evaluate RL actors or critics. If interrupted, resume from the per-block checkpoints; do not restart with replacement seeds.

The run's scientific purpose is to estimate

\[
\mu_L(r_{t-1})=E_L[r_t\mid r_{t-1}]
\]

and corresponding conditional variance/tail diagnostics under the frozen SBJTS law and the iid empirical-Merton control. The Merton conditional-mean curve should remain flat within Monte Carlo uncertainty; the SBJTS curve is descriptive mechanism evidence whatever its shape.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- `reports/pmo/PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`
- `reports/pmo/PMO_CONDLAW_CODE_AUDIT_v1.md`
- `reports/pmo/PMO_CONDLAW_CODE_ACCEPTANCE_v2.md`
- `evidence/theory_coupling_v1/unit_checks.json`
- `evidence/theory_coupling_v1/theorem_code_map.csv`
- `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`
- `evidence/merton_comparator_v1/research/policy_response_surface.csv`
- `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
- `evidence/merton_comparator_v1/research/policy_level_sensitivity.csv`

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- `C-RLSBJTS-MERTON-COMP-01` completed its scientific purpose; the user-Colab T4 evidence is accepted with scope under DEC-RL-004.
- `C-RLSBJTS-THEORY-COUPLING-01` completed its scientific purpose under `PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`.
- Conditional-law submission `e60a351...` is superseded by accepted patched code `c47304c...`.
- Historical theory submissions `64cd35b0...` and `6bc4796...` are superseded by `ed7e9b5...`.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- The process rule from DEC-RL-002 remains binding: Claude does derivation/design/code/smoke; the user owns future research-scale Colab execution.
