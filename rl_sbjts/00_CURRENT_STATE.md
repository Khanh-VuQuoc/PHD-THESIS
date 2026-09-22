# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **SCIENTIFIC_BACKBONE_LOCKED / MANUSCRIPT_INTEGRATION** — direct comparator, T1–T5 theory, robustness, saved-policy mechanism evidence, and the user-Colab conditional-law diagnostic are accepted with stated scope. No further research-scale experiment is open. |
| Executable research ticket | **NONE. STOP EXPERIMENTS.** `C-RLSBJTS-CONDLAW-DIAG-01` has completed its scientific purpose. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL comparator result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 comparator result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Comparator robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Theory status | **ACCEPTED_WITH_STATED_ASSUMPTIONS.** T1 exact wealth coupling; T2 moment/path-law non-equivalence; T3 history-state likelihood-ratio gradient without assuming the four-feature observation is Markov; T4 symmetric occupancy/continuation-value decomposition; T5 structural lagged-return mechanism; entropy scaling `m=lambda*dt`. |
| T3 regularity | The theorem is conditional on A4, or the sufficient mixed condition `sup_theta E[(1+max_t||S_t||)(1+|R_soft|)] < infinity`; this is assumed, not claimed verified for the frozen SBJTS law. |
| Saved-policy mechanism evidence | Average executed exposure is nearly unchanged, while saved SBJTS actors show strong negative lag-return and wealth-state feedback and Merton actors are nearly flat. FULL lag-response slope is about `-0.674` for SBJTS vs `+0.015` for Merton. |
| Conditional-law result | **ACCEPTED_EXPLORATORY_MECHANISM_EVIDENCE.** User T4 run completed `64 × 3,072` paths per law and `4,000` block-bootstrap replicates. SBJTS lag slope `-0.125006` with 95% CI `[-0.125843,-0.124150]`; lag-1 autocorrelation `-0.124750` with CI `[-0.125587,-0.123909]`. Merton research slope `+0.000135` with CI `[-0.000430,+0.000716]`. |
| Conditional-risk result | SBJTS also shows state-dependent variance and left-tail probability. Variance rises to `0.0009073` after the most negative lag bin and `0.0004576` after the most positive lag bin versus unconditional `0.0002623`; the fixed-Merton 5% tail probability ranges from about `2.8–3.2%` after negative lags to `7.85%` after the most positive lag. Merton remains approximately flat. |
| Conditional-law hardware/provenance | Research evidence is correctly stamped `C-RLSBJTS-CONDLAW-DIAG-01`, executed on Tesla T4 / CUDA 12.8 / `TORCH_CUDA_FLOAT32_BATCHED`; Base-3 code concat, snapshot, training slice and environment fingerprints match the frozen lineage. |
| Result audit | `reports/pmo/PMO_CONDLAW_RESULT_AUDIT_v1.md` — `RESEARCH_EVIDENCE_ACCEPTED_WITH_SCOPE / STOP_EXPERIMENTS`. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim, no claim that lagged return alone causes the observed gain. |
| Next PMO action | Integrate comparator + theory + mechanism into the manuscript; generate final figures/tables; update the TeX; perform claim/limitation and reference audit. |

## Locked scientific narrative

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

The evidence chain is complete for the intended domain-scoped paper claim:

1. **Path-law evidence.** Base 4 shows that matching local canonical mean/variance does not match terminal/path behavior; cross-time dependence matters.
2. **Direct performance evidence.** On the same frozen SBJTS deployment law, the SBJTS-trained learner has higher terminal log wealth and lower CVaR log loss than the matched empirical-Merton/GBM-trained learner under both frozen constraints.
3. **Theory.** T1–T5 establish how a market law can enter wealth dynamics, policy gradients, occupancy and continuation values without assuming the learner's four-feature observation is a complete Markov state.
4. **Saved-policy mechanism evidence.** Merton-trained policies are almost flat in lagged return while SBJTS-trained policies learn strong negative lag feedback.
5. **Direct conditional-law evidence.** The frozen SBJTS market object has pronounced negative lag dependence and state-dependent variance/tail risk, while the iid Merton control is recovered as flat. The SBJTS policy response is qualitatively aligned with that target-law structure.

The final mechanism claim is descriptive rather than causal: the conditional/path structure provides information that can support a different feedback policy, but the experiment does not identify a unique causal share of the wealth/CVaR gap attributable to lagged return alone.

## Manuscript-safe conditional-law statement

> In the frozen target simulator, the projected risky return exhibits pronounced lag-dependent conditional mean, variance and left-tail risk, whereas the matched empirical-Merton law is flat by construction and is recovered as flat in the simulation control. The SBJTS-trained policies exhibit feedback to lagged return in a direction qualitatively consistent with this target-law structure, while Merton-trained policies are nearly insensitive to the lagged-return state. This is descriptive mechanism evidence, not causal attribution of the performance gap to a single state variable.

When plotting conditional means, use within-law deviations or each law's own unconditional reference line when interpreting temporal structure. Do not attribute raw cross-law conditional-mean level differences solely to dependence because the direct comparator laws do not have identical unconditional means.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- `reports/pmo/PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`
- `reports/pmo/PMO_CONDLAW_CODE_ACCEPTANCE_v2.md`
- `reports/pmo/PMO_CONDLAW_RESULT_AUDIT_v1.md`
- `evidence/theory_coupling_v1/unit_checks.json`
- `evidence/theory_coupling_v1/theorem_code_map.csv`
- `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`
- `evidence/merton_comparator_v1/research/policy_response_surface.csv`
- `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
- `evidence/merton_comparator_v1/research/policy_level_sensitivity.csv`

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- `C-RLSBJTS-MERTON-COMP-01` completed its scientific purpose under DEC-RL-004.
- `C-RLSBJTS-THEORY-COUPLING-01` completed its scientific purpose under `PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`.
- `C-RLSBJTS-CONDLAW-DIAG-01` completed its scientific purpose under `PMO_CONDLAW_RESULT_AUDIT_v1.md`.
- Conditional-law code submission `e60a351...` is superseded by accepted patched code `c47304c...`.
- Historical theory submissions `64cd35b0...` and `6bc4796...` are superseded by `ed7e9b5...`.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- Process rule DEC-RL-002 remains binding for any future work: Claude does derivation/design/code/smoke; the user owns research-scale execution. No new research-scale work is currently authorized.
