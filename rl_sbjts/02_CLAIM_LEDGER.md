# 02_CLAIM_LEDGER — RL–SBJTS

Updated: 2026-09-21. PMO authority: `00_CURRENT_STATE.md`.

| ID | Claim | Status | Evidence / qualification |
|---|---|---|---|
| CL-RL-001 | The Base 4 execution completed cleanly under its frozen design. | **SUPPORTED** | 160/160 training attempts and 96,000/96,000 evaluation attempts completed; frozen audit/handover. |
| CL-RL-002 | Under Base 4, target-SBJTS training and affine-calibrated no-jump-control training yield different target-holdout portfolio outcomes. | **SUPPORTED_ESTIMATION_FIRST** | Signed TT-CT effects and crossed-bootstrap intervals; no prospective numeric SESOI. |
| CL-RL-003 | Base 4 isolates a pure Bernoulli jump effect. | **BLOCKED** | Target/control differ in temporal dependence and higher-order structure; only canonical one-step mean/variance were matched. |
| CL-RL-004 | Base 4 proves full training-risk distributions are matched. | **BLOCKED** | Terminal variance and higher-order/path properties are not matched. |
| CL-RL-005 | Cross-time covariance/dependence explains the residual terminal-variance gap after local variance matching. | **SUPPORTED_WITH_SCOPE** | F-032 decomposition identity verified on 20/20 seeds; no attribution to a specific bridge subcomponent. |
| CL-RL-006 | RL–SBJTS is superior to RL–Merton/GBM. | **NOT_TESTED** | No direct Merton/GBM training-law arm exists in frozen Base 4. This is the purpose of `C-RLSBJTS-MERTON-COMP-01`. |
| CL-RL-007 | RL–SBJTS is universally superior to Merton across markets, learners, constraints, and exploration levels. | **BLOCKED** | A single target environment/learner/`m` cannot support a universal claim. |
| CL-RL-008 | The exploratory Merton RL implementation is mathematically meaningful as a positive control. | **SUPPORTED_AS_DESIGN / NUMERIC_RECOVERY_NOT_PROMOTED_HERE** | Base 1 defines the GBM/Merton oracle; executed numerical recovery values are not promoted by the current source set. |
| CL-RL-009 | A learned RL–Merton policy can be compared fairly with RL–SBJTS on the frozen SBJTS holdout if training data, learner, constraints, budget, evaluation seeds and action uniforms are held fixed appropriately. | **PROSPECTIVE_DESIGN** | Must be demonstrated by the comparator ticket before promotion. |
| CL-RL-010 | Any future RL–SBJTS vs RL–Merton difference is a pure jump effect. | **BLOCKED** | It is a model/environment-misspecification or training-law contrast unless additional component isolation is designed. |
| CL-RL-011 | The current study establishes external empirical market validity of SBJTS. | **BLOCKED** | Frozen Base 2 ancestry is smoke-scale; the study is conditional on that environment. |
| CL-RL-012 | A direct comparator may be written as confirmatory superiority after seeing the result. | **BLOCKED** | No retrospective SESOI or post-result confirmatory gate may be invented. A future confirmatory design would require prospective justification before execution. |

## Promotion rule for the Merton comparator

`CL-RL-006` may move only from `NOT_TESTED` to a narrow evidence-scoped status after PMO independently verifies:

1. Merton/GBM calibration used only the frozen training slice;
2. no target holdout information entered calibration/training/selection;
3. learner/action constraints/exploration/budget are aligned;
4. frozen Base 4 target-evaluation randomness is reproduced or an explicitly prospective new paired holdout namespace is used;
5. all failed/partial runs remain in the denominator/accounting;
6. effect estimates and uncertainty are reported by constraint stratum;
7. the conclusion is limited to the tested target environment and learner.
