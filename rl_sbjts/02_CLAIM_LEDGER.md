# 02_CLAIM_LEDGER — RL–SBJTS

Updated: 2026-09-22. PMO authority: `00_CURRENT_STATE.md`.

| ID | Claim | Status | Evidence / qualification |
|---|---|---|---|
| CL-RL-001 | The Base 4 execution completed cleanly under its frozen design. | **SUPPORTED** | 160/160 training attempts and 96,000/96,000 evaluation attempts completed; frozen audit/handover. |
| CL-RL-002 | Under Base 4, target-SBJTS training and affine-calibrated no-jump-control training yield different target-holdout portfolio outcomes. | **SUPPORTED_ESTIMATION_FIRST** | Signed TT-CT effects and crossed-bootstrap intervals; no prospective numeric SESOI. |
| CL-RL-003 | Base 4 isolates a pure Bernoulli jump effect. | **BLOCKED** | Target/control differ in temporal dependence and higher-order structure; only canonical one-step mean/variance were matched. |
| CL-RL-004 | Base 4 proves full training-risk distributions are matched. | **BLOCKED** | Terminal variance and higher-order/path properties are not matched. |
| CL-RL-005 | Cross-time covariance/dependence explains the residual terminal-variance gap after local variance matching. | **SUPPORTED_WITH_SCOPE** | F-032 decomposition identity verified on 20/20 seeds; no attribution to a specific bridge subcomponent. |
| CL-RL-006 | RL–SBJTS outperforms RL–Merton/GBM under the tested frozen SBJTS deployment law. | **SUPPORTED_WITH_SCOPE** | Direct learned-arm comparator on the same frozen SBJTS target holdout: FULL `Delta_W=+0.0022063`, `Delta_CVaR=-0.0031810`; CAP50 `Delta_W=+0.0005541`, `Delta_CVaR=-0.0007611`. Frozen crossed-cluster 95% intervals exclude zero for all four contrasts; policy-level sensitivity using only 40 paired training replications also excludes zero, with favorable sign in 40/40 replications in every endpoint/stratum. Domain-scoped only; no universal claim. |
| CL-RL-007 | RL–SBJTS is universally superior to Merton across markets, learners, constraints, and exploration levels. | **BLOCKED** | A single target environment/learner/`m` cannot support a universal claim. |
| CL-RL-008 | The exploratory Merton RL implementation is mathematically meaningful as a positive control. | **SUPPORTED_WITH_SCOPE** | The user-Colab comparator passed the bounded empirical-Merton learner positive control; analytic-Merton interpretation remains subject to the discrete-versus-continuous entropy-time-scale distinction. |
| CL-RL-009 | A learned RL–Merton policy can be compared fairly with RL–SBJTS on the frozen SBJTS holdout under aligned learner, constraints, budget and evaluation namespace. | **SUPPORTED_EXECUTED** | User Colab T4 run completed 80/80 Merton policies, 24,000/24,000 MT evaluations, reused 24,000 frozen TT rows, and passed the predeclared two-holdout reproduction gate bitwise exactly. |
| CL-RL-010 | The RL–SBJTS vs RL–Merton difference is a pure jump effect. | **BLOCKED** | It is a training-law/model-misspecification contrast unless additional component isolation is designed. |
| CL-RL-011 | The current study establishes external empirical market validity of SBJTS. | **BLOCKED** | Frozen Base 2 ancestry is smoke-scale; the study is conditional on that environment. |
| CL-RL-012 | The direct comparator may be rewritten as confirmatory superiority after seeing the result. | **BLOCKED** | No retrospective SESOI or post-result confirmatory gate may be invented. A future confirmatory design would require prospective justification before execution. |
| CL-RL-013 | SBJTS and Merton training produce materially different state-feedback policies even though their average risky exposure is nearly the same. | **SUPPORTED_MECHANISM_EVIDENCE** | Saved-policy response surfaces show strong negative SBJTS sensitivity to lagged return and wealth state while Merton policies are nearly flat. FULL local lag-return slope of executed mean action is about `-0.674` for SBJTS vs `+0.015` for Merton; CAP50 `-0.210` vs `+0.006`. This is mechanism evidence, not sole-cause attribution. |
| CL-RL-014 | Lagged return alone causes the entire SBJTS performance gain. | **NOT_ESTABLISHED / BLOCKED_AS_CAUSAL_CLAIM** | Current evidence shows a strong policy-response channel but does not isolate lagged return from occupancy, continuation-value, wealth-state, or other path-law effects. |

## Scope of the accepted direct-comparator evidence

The supported statement is deliberately narrow:

> Under the tested frozen SBJTS deployment environment, an RL policy trained under the frozen SBJTS market law achieved higher terminal log wealth and lower CVaR log loss than an otherwise matched RL policy trained under the empirical Merton/GBM law, in both frozen long-only constraint strata.

This is **not** a statement of universal superiority, a pure-jump causal effect, external-market validity, or a retrospectively confirmatory superiority claim.

## Next promotion target

The next research bottleneck is theory coupling rather than additional training. `C-RLSBJTS-THEORY-COUPLING-01` must formalize:

1. exact wealth-law coupling;
2. moment-matching non-equivalence;
3. trajectory policy gradient under history dependence / partial observation;
4. occupancy and continuation-value channels;
5. theorem-to-code verification and cheap gate-mutation tests.
