# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-22. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **THEORY_ACCEPTED / CONDLAW_CODE_PATCH_REQUESTED** — the direct comparator and T1–T5 theory backbone are accepted. The conditional-law diagnostic design is accepted in substance, but two narrow code/provenance issues must be patched before any user Colab RESEARCH run. |
| Sole executable ticket | `tickets/C-RLSBJTS-CONDLAW-DIAG-01.md` — patch the current `e60a351...` submission only; no research-scale execution by Claude. |
| Closed theory ticket | `tickets/C-RLSBJTS-THEORY-COUPLING-01.md` — final submission `ed7e9b5a15bdc1c52c309fc6b3165943fe225ed8` accepted by PMO. |
| Accepted empirical scope | Under the tested frozen SBJTS deployment law, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than otherwise matched empirical-GBM-trained policies in both LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| FULL result | `Delta_W = +0.0022063`; `Delta_CVaR = -0.0031810`. |
| CAP50 result | `Delta_W = +0.0005541`; `Delta_CVaR = -0.0007611`. |
| Robustness | Frozen crossed-cluster 95% intervals exclude zero for all four co-primary contrasts. Policy-level sensitivity using only the 40 paired training replications also excludes zero for all four; favorable sign is 40/40 in every endpoint/stratum. |
| Mechanism evidence | Average executed exposure is nearly unchanged, while saved SBJTS actors show strong negative lag-return and wealth-state feedback and Merton actors are nearly flat. FULL lag-response slope ≈ `-0.674` for SBJTS vs `+0.015` for Merton. |
| Theory status | **ACCEPTED_WITH_STATED_ASSUMPTIONS.** T1 exact wealth coupling; T2 moment/path-law non-equivalence; T3 history-state likelihood-ratio gradient without assuming the four-feature observation is Markov; T4 symmetric occupancy/continuation-value decomposition; T5 structural lagged-return mechanism; entropy scaling `m=lambda*dt`. |
| T3 regularity | The theorem is conditional on A4, or the sufficient mixed condition `sup_theta E[(1+max_t||S_t||)(1+|R_soft|)] < infinity`; this is assumed, not claimed verified for the frozen SBJTS law. |
| Conditional-law code audit | Submission `e60a3513b358064c953597a4e0e81519209239a7` is **TARGETED_PATCH_BEFORE_COLAB**. Design, bins, block-bootstrap unit, controls, resumability, no-training scope, and proposed budget are accepted. Blocking P1: diagnostic artifacts are incorrectly stamped with the old comparator ticket. Blocking P2: notebook unnecessarily stages raw comparator/Base4 policy/training/evaluation ledgers, including an unpinned size-selected TT ledger, even though the market-only diagnostic does not need them. |
| Approved-in-principle diagnostic budget | `64 blocks × 3,072 paths per law`, `4,000` block-bootstrap replicates, `TORCH_CUDA_FLOAT32_BATCHED` on paid Colab T4, up to 45 minutes. **Not yet authorized to run** until P1–P2 clear PMO code re-audit. |
| Diagnostic audit note | `reports/pmo/PMO_CONDLAW_CODE_AUDIT_v1.md`. |
| Evidence location | User Colab T4 comparator raw outputs remain on Drive under `merton_comparator_v1/evidence/research/`; GitHub pins their Drive IDs, byte sizes and SHA-256 in `evidence/merton_comparator_v1/research/ARTIFACT_MANIFEST.json`. |
| Permanent limitations | No universal superiority, no pure-jump causal attribution, no external-market validity from smoke-scale Base 2 ancestry, no retrospective confirmatory-superiority claim, no claim that lagged return alone causes the observed gain. |
| Next PMO decision | Re-audit Claude's narrow conditional-law code patch. If P1–P2 are clean and controls still pass, merge/accept code and authorize the user-only T4 market-simulation diagnostic. |

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

The remaining empirical mechanism task is intentionally narrow: characterize the frozen conditional return law directly. No policy retraining is needed.

## Sole open ticket

`C-RLSBJTS-CONDLAW-DIAG-01` remains the only executable work package.

The first code submission `e60a351...` is accepted in scientific design but requires two targeted corrections before Colab authorization:

### P1 — correct diagnostic provenance

Every SMOKE/RESEARCH artifact produced by the diagnostic must identify

```text
ticket = C-RLSBJTS-CONDLAW-DIAG-01
claim_status = EXPLORATORY_MECHANISM_ONLY
```

with the appropriate run mode/evidence class. The old `C-RLSBJTS-MERTON-COMP-01` producer ticket must not appear in diagnostic output metadata. Add a cheap gate that catches a stale producer-ticket namespace.

### P2 — remove irrelevant raw comparator dependencies

The market-only diagnostic must not unconditionally stage/read raw `policies.npz`, `training_attempts.csv`, or the large `evaluation_results_partial.csv` ledger merely because comparator modules were reused. The policy overlay should consume the already-accepted compact policy-response evidence, pinned by content. Any larger input that is truly executed must be justified and content-pinned; do not resolve scientific evidence by filename/size ambiguity.

Claude may rerun only cheap unit/smoke checks. No RESEARCH mode is authorized during the patch.

## Evidence references

- `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
- `reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- `reports/pmo/PMO_THEORY_COUPLING_ACCEPTANCE_v3.md`
- `reports/pmo/PMO_CONDLAW_CODE_AUDIT_v1.md`
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
- Historical theory submissions `64cd35b0...` and `6bc4796...` are superseded by `ed7e9b5...`.
- Commit `0bdd16b` remains **DEVELOPMENT_EVIDENCE** only.
- The process rule from DEC-RL-002 remains binding: Claude does derivation/design/code/smoke; the user owns future research-scale Colab execution.
