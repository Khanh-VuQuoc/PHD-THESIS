# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **THEORY_COUPLING_FINAL_PATCH_REQUESTED** — the empirical comparator remains accepted; Claude's P1–P5 theory patch is accepted in substance, with one final regularity correction P6 required before manuscript adoption. |
| Sole executable ticket | `tickets/C-RLSBJTS-THEORY-COUPLING-01.md` — remains `PATCH_REQUESTED`; no new research-scale execution is authorized. |
| Closed empirical question | Direct learned RL–SBJTS vs empirical RL–Merton/GBM on the same frozen SBJTS target holdout. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Mechanism evidence | Average exposure is nearly unchanged, but saved SBJTS actors show strong negative lag-return and wealth-state feedback while Merton actors are nearly flat. FULL executed-action lag slope ≈ `-0.674` for SBJTS vs `+0.015` for Merton. |
| Theory audit | P1–P5 are accepted: local T1 expansion, corrected market-entry wording, explicit domination assumption, corrected finite-difference language, and symmetric T4 decomposition. Remaining P6: the T3 regularity discussion must not claim the actor score is uniformly bounded solely from the bounded policy transform, because `grad_theta log lambda` chains through the state features. Replace the reduction to `E|X_N-X_0|<∞` with an explicit mixed state/return domination condition. |
| Base 4 retained finding | Local one-step mean/variance similarity does not remove path/terminal differences; cross-time covariance/dependence explains the residual terminal-variance gap at decomposition level. |
| Evidence location | User Colab T4 raw outputs remain on Drive under `merton_comparator_v1/evidence/research/`; GitHub pins Drive IDs, byte sizes and SHA-256 in `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`. |
| Research hardware lineage | Paid Colab NVIDIA T4; frozen market engine CUDA float32 batched; frozen Base 3 learner update path NumPy float64 CPU for numerical comparability. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim. |
| Next PMO decision | Audit the final P6 theory wording patch. If it clears, accept/merge the theory backbone and move to lightweight conditional-law diagnostics/manuscript integration. |

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

The theory backbone is now nearly complete. The only remaining correction is a regularity/notation point in T3; no additional training is needed.

## Sole open ticket

`C-RLSBJTS-THEORY-COUPLING-01` remains the sole executable ticket. Claude's patch commit `6bc47961f9a3be4ddef1101c98d6c2100364845d` satisfies P1–P5. PMO audit v2 is recorded in:

- `reports/pmo/PMO_THEORY_COUPLING_PATCH_AUDIT_v2.md`

### Final required patch P6

The report currently treats the actor score `psi_theta = grad_theta log lambda_theta(A_t|S_t)` as uniformly bounded once the executed location/scale are bounded. That skips the chain through the actor state features. For the frozen linear actor,

\[
\nabla_\theta \log\lambda_\theta
=
\nabla_\phi\log\lambda_\phi\;J_{\mathrm{transform}}\;\nabla_\theta(\Theta S_t),
\]

and the final factor contains `S_t`, including `log(W_t/W_0)` and `r_{t-1}`. Therefore the theorem should keep a direct domination assumption or use an explicit sufficient mixed-moment condition such as

\[
E\Big[(1+\max_t\|S_t\|)(1+|R^{soft}|)\Big]<\infty
\]

uniformly on a local parameter neighbourhood. Do not reduce A4 to terminal-log-wealth first-moment integrability alone unless additional state bounds are proved. The theorem-to-code map should distinguish `score_phi` from the full actor-weight score.

Claude remains **smoke/unit only**. No research-scale training/evaluation is authorized.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/research/RL_SBJTS_THEORY_COUPLING_BLUEPRINT_v1.md`
- `reports/pmo/PMO_THEORY_COUPLING_PATCH_AUDIT_v2.md`
- `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`
- `evidence/merton_comparator_v1/research/policy_response_surface.csv`
- `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
- `evidence/merton_comparator_v1/research/policy_level_sensitivity.csv`

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- `C-RLSBJTS-MERTON-COMP-01` has completed its scientific purpose; its user-Colab T4 research evidence is accepted with scope under DEC-RL-004.
- Theory submission `64cd35b0...` is superseded by patched candidate `6bc4796...`; the latter is accepted in substance except for final P6 regularity wording.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- The process rule from DEC-RL-002 remains binding: Claude does derivation/design/code/smoke; the user owns any future research-scale Colab execution.
