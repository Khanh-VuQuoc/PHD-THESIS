# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **THEORY_COUPLING_PATCH_REQUESTED** — the direct RL–SBJTS versus RL–Merton/GBM empirical comparator remains accepted as scoped research evidence; Claude's theory package is substantively strong but needs a narrow mathematical wording/decomposition patch before manuscript adoption. |
| Sole executable ticket | `tickets/C-RLSBJTS-THEORY-COUPLING-01.md` — `PATCH_REQUESTED`. |
| Closed empirical question | Direct learned RL–SBJTS vs empirical RL–Merton/GBM on the same frozen SBJTS target holdout. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Mechanism evidence | Average exposure is nearly unchanged, but saved SBJTS actors show strong negative lag-return and wealth-state feedback while Merton actors are nearly flat. FULL executed-action lag slope ≈ `-0.674` for SBJTS vs `+0.015` for Merton. |
| Theory audit | T1–T5 core derivations, theorem-to-code map and mutation tests are accepted in substance. Required patch: localize the Taylor/moment-series statement, state explicit integrability assumptions for the policy-gradient theorem, remove the claim that central finite differences are unbiased, soften the claim that the market enters the learning problem only through wealth coupling, and use a symmetric/reference-explicit T4 decomposition in the manuscript. |
| Base 4 retained finding | Local one-step mean/variance similarity does not remove path/terminal differences; cross-time covariance/dependence explains the residual terminal-variance gap at decomposition level. |
| Evidence location | User Colab T4 raw outputs remain on Drive under `merton_comparator_v1/evidence/research/`; GitHub pins Drive IDs, byte sizes and SHA-256 in `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`. |
| Research hardware lineage | Paid Colab NVIDIA T4; frozen market engine CUDA float32 batched; frozen Base 3 learner update path NumPy float64 CPU for numerical comparability. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim. |
| Next PMO decision | Audit the targeted theory patch. If it clears, merge the theory package and decide whether only a lightweight conditional-law diagnostic is needed before manuscript lock; no retraining is currently authorized. |

## Current scientific narrative

The paper is now organized around

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

The empirical backbone is already in place:

1. **Path-law evidence:** Base 4 shows that matching local canonical mean/variance does not match terminal/path behavior.
2. **Direct performance evidence:** RL–SBJTS outperforms matched RL–Merton/GBM on the frozen SBJTS deployment law in both wealth and CVaR loss under both constraints.
3. **Mechanism evidence:** the performance difference is not explained by average exposure; the saved policies encode materially different feedback to lagged return and current wealth.

The remaining high-value work is theoretical formalization and lightweight mechanism verification, not another full training campaign.

## Sole open ticket

`C-RLSBJTS-THEORY-COUPLING-01` remains the sole executable ticket. Claude's first submission proved the core T1–T5 package and passed cheap theorem-to-code/mutation tests, but PMO requires a targeted patch before manuscript adoption:

- T1 Taylor/moment expansion must be stated as local/asymptotic (or under explicit convergence/interchange conditions), while the exact wealth coupling remains global;
- T1 wording must say the market enters the **one-step wealth increment** through `g(A_t,r_t)` while the market law also determines future history/state occupancy and continuation values;
- T3 regularity must use explicit integrability/domination assumptions rather than claiming the SBJTS return law has bounded support;
- T3.4 must describe central finite difference as a numerical approximation with truncation error, not an unbiased estimator;
- T4 should adopt a symmetric midpoint decomposition for the main manuscript, or otherwise state the reference convention explicitly and demonstrate the symmetric version on the enumerable fixture;
- no new research-scale execution is allowed.

Claude remains **smoke/unit only**. No research-scale training/evaluation is authorized for the theory patch.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/research/RL_SBJTS_THEORY_COUPLING_BLUEPRINT_v1.md`
- `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`
- `evidence/merton_comparator_v1/research/policy_response_surface.csv`
- `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
- `evidence/merton_comparator_v1/research/policy_level_sensitivity.csv`

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- `C-RLSBJTS-MERTON-COMP-01` has completed its scientific purpose; its user-Colab T4 research evidence is accepted with scope under DEC-RL-004.
- Theory submission commit `64cd35b0d885a5306733a5c7ea4ea75a8ba0fd18` is retained as the first theory candidate; it is not yet merged/adopted because DEC-RL-005 requests a targeted mathematical patch.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- The process rule from DEC-RL-002 remains binding: Claude does derivation/design/code/smoke; the user owns any future research-scale Colab execution.