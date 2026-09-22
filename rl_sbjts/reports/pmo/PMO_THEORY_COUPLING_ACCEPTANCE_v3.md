# PMO Theory Coupling Acceptance v3

**Date:** 2026-09-22  
**Submission:** `ed7e9b5a15bdc1c52c309fc6b3165943fe225ed8`  
**Verdict:** `ACCEPTED_WITH_STATED_ASSUMPTIONS`

## Decision

The T1–T5 theory-coupling package is accepted for manuscript integration. P6 closes the last blocking regularity issue from the prior audit. No further theory patch is required before manuscript drafting.

The accepted backbone is conditional where it must be conditional: the likelihood-ratio gradient theorem assumes the explicit domination condition A4 (or the sufficient mixed state/soft-return moment condition A4-mixed); this condition is not claimed to have been proved for the frozen SBJTS law.

## P6 audit

P6 correctly separates two scores that were previously conflated:

1. the policy-parameter score `psi_phi = grad_phi log lambda`, which is bounded on the frozen location/scale box; and
2. the full actor-weight score `grad_theta log lambda`, which chains through the linear state map and therefore carries a factor of `S_t`.

For the frozen actor,

\[
\nabla_{w_k}\log\lambda_θ(A_t\mid S_t)
=
\big[J_{\rm transform}(\mathrm{raw}_t)^\top\psi_\phi(A_t,S_t)\big]_k S_t.
\]

Because `S_t=(1,t/N,log(W_t/W_0),r_{t-1})` is not globally bounded, bounded executed policy parameters alone do not imply a uniformly bounded actor-weight score. The new `t3_6` fixture verifies the chain rule against actor-weight finite differences with worst relative error `3.0e-09`, and gives an explicit witness where the actor-weight score grows proportionally to the state norm while the policy-parameter score remains constant.

The replacement regularity condition is manuscript-safe:

\[
\sup_{\theta\in U}
E\Big[(1+\max_{t\le N}\|S_t\|)(1+|R^{\rm soft}_\theta|)\Big]<\infty.
\]

This is appropriately presented as a sufficient assumption on the training law, not as an empirically verified property of the frozen SBJTS engine.

The zero-score lemma remains valid because the raw-to-policy Jacobian and `S_t` are `S_t`-measurable, so `E[psi_phi|S_t]=0` transfers to the actor-weight score.

## Verification retained

- frozen source identity remains pinned;
- 20 gated check groups pass;
- 19 theorem-to-code rows pass;
- the `all_pass` aggregator now derives its gate set from the computed checks rather than a stale hard-coded list;
- the only intentionally non-gated block is `t1_moment_structure`, which is a record rather than a test;
- no research-scale training/evaluation or empirical estimand was produced by this theory package.

## Accepted manuscript theory

The manuscript may now use:

- **T1:** exact global wealth coupling, with Taylor/moment expansion only locally/asymptotically or under stated convergence conditions;
- **T2:** equality of local unconditional mean/variance is insufficient for RL equivalence in general;
- **T3:** likelihood-ratio policy gradient for an observation-based policy on a history-state process, without assuming the four-feature observation is Markov, conditional on A1–A4;
- **T4:** symmetric midpoint occupancy/continuation-value decomposition under a common dominating measure, explicitly as an attribution convention rather than causal identification;
- **T5:** lagged-return predictability is structurally unavailable under iid Merton but can be available under a history-dependent SBJTS law; this is a mechanism-availability result, not sole-cause attribution;
- entropy scaling `m = lambda * dt`.

## Non-blocking editorial note

The historical patch-response table still contains an old P3 summary sentence saying A4 was reduced to first-moment terminal-log-wealth integrability. That sentence is superseded by P6 and by the final T3 assumptions, which explicitly withdraw that reduction. It must not be copied into the manuscript. This is editorial history, not a remaining theory defect.

## Remaining scientific gap

The only high-value mechanism gap is empirical, not theoretical: directly characterize the frozen SBJTS conditional law, especially

\[
\mu_S(r_{t-1})=E_S[r_t\mid r_{t-1}],
\]

and compare it with the flat iid-Merton benchmark. A lag-ablation retraining experiment is **not** required for the current paper claim and is not authorized at this stage.

## PMO action

Theory gate closed. Next action is one lightweight, no-retraining conditional-law diagnostic, followed by manuscript integration.
