# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **THEORY_ACCEPTED / CONDITIONAL_LAW_DIAGNOSTIC_OPEN** — the direct comparator and the T1–T5 theory backbone are accepted with stated scope/assumptions. The remaining high-value task is a lightweight no-retraining conditional-law mechanism diagnostic before manuscript lock. |
| Sole executable ticket | `tickets/C-RLSBJTS-CONDLAW-DIAG-01.md` — `OPEN_FOR_CLAUDE`. |
| Closed theory ticket | `tickets/C-RLSBJTS-THEORY-COUPLING-01.md` — final submission `ed7e9b5a15bdc1c52c309fc6b3165943fe225ed8` accepted by PMO; no further theory patch required. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Mechanism evidence | Average exposure is nearly unchanged, but saved SBJTS actors show strong negative lag-return and wealth-state feedback while Merton actors are nearly flat. FULL executed-action lag slope ≈ `-0.674` for SBJTS vs `+0.015` for Merton. |
| Theory status | **ACCEPTED_WITH_STATED_ASSUMPTIONS.** T1 exact wealth coupling; T2 moment/path-law non-equivalence; T3 history-state likelihood-ratio gradient without assuming the four-feature observation is Markov; T4 symmetric occupancy/continuation-value decomposition; T5 structural lagged-return mechanism; entropy scaling `m=lambda*dt`. |
| T3 regularity | Final P6 distinguishes bounded policy-parameter score `psi_phi` from the full actor-weight score, which chains through `S_t`. The gradient theorem is conditional on A4, or the sufficient mixed condition `sup_theta E[(1+max_t||S_t||)(1+|R_soft|)] < infinity`; this is assumed, not claimed verified for the frozen SBJTS law. |
| Theory verification | 20 gated check groups pass; 19 theorem-to-code rows pass; frozen source identity remains pinned; no research-scale computation occurred in the theory package. |
| Base 4 retained finding | Local one-step mean/variance similarity does not remove path/terminal differences; cross-time covariance/dependence explains the residual terminal-variance gap at decomposition level. |
| Evidence location | User Colab T4 raw outputs remain on Drive under `merton_comparator_v1/evidence/research/`; GitHub pins Drive IDs, byte sizes and SHA-256 in `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`. |
| Research hardware lineage | Paid Colab NVIDIA T4; frozen market engine CUDA float32 batched; frozen Base 3 learner update path NumPy float64 CPU for numerical comparability. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim, no claim that lagged return alone causes the observed gain. |
| Next PMO decision | Audit Claude's no-retraining conditional-law diagnostic code/smoke package. If accepted, user may run only the bounded market-simulation diagnostic in Colab; lag-ablation retraining remains unauthorized. |

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

The scientific backbone is now in place:

1. **Path-law evidence:** Base 4 shows that matching local canonical mean/variance does not match terminal/path behavior.
2. **Direct performance evidence:** RL–SBJTS outperforms matched RL–Merton/GBM on the frozen SBJTS deployment law in wealth and CVaR loss under both frozen constraints.
3. **Mechanism evidence:** the gain is not explained by average risky exposure; the saved policies encode materially different feedback to lagged return and current wealth.
4. **Theory:** T1–T5 formally connect the market law to wealth increments, policy gradients, state occupancy, continuation values and lagged-return information, with all regularity assumptions stated explicitly.

The remaining mechanism task is intentionally narrow: estimate the frozen conditional return law directly and compare it with the flat iid-Merton benchmark. No policy retraining is needed.

## Sole open ticket

`C-RLSBJTS-CONDLAW-DIAG-01` asks Claude to design/implement/smoke a lightweight diagnostic that estimates

\[
\mu_S(r_{t-1})=E_S[r_t\mid r_{t-1}]
\]

and corresponding conditional variance/tail diagnostics from frozen market simulation only, using a common fixed binning scheme and seed/block-level uncertainty. The accepted saved-policy response is overlaid descriptively; no actor/critic retraining is allowed.

Claude remains **smoke/unit only**. If research-scale simulation is needed, the user executes it in Colab after PMO code review.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- `reports/pmo/PMO_THEORY_COUPLING_PATCH_AUDIT_v2.md`
- `reports/pmo/PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`
- `evidence/theory_coupling_v1/unit_checks.json`
- `evidence/theory_coupling_v1/theorem_code_map.csv`
- `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`
- `evidence/merton_comparator_v1/research/policy_response_surface.csv`
- `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
- `evidence/merton_comparator_v1/research/policy_level_sensitivity.csv`

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- `C-RLSBJTS-MERTON-COMP-01` completed its scientific purpose; the user-Colab T4 evidence is accepted with scope under DEC-RL-004.
- `C-RLSBJTS-THEORY-COUPLING-01` completed its scientific purpose. Submission `ed7e9b5a15bdc1c52c309fc6b3165943fe225ed8` is accepted under `PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`.
- Historical theory submissions `64cd35b0...` and `6bc4796...` are superseded by `ed7e9b5...`.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- The process rule from DEC-RL-002 remains binding: Claude does derivation/design/code/smoke; the user owns future research-scale Colab execution.
