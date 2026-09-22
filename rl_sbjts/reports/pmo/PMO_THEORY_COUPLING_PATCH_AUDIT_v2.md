# PMO theory-coupling patch audit v2

Date: 2026-09-22

Submission audited: `6bc47961f9a3be4ddef1101c98d6c2100364845d`

## Verdict

`TARGETED_PATCH_P6`

The requested P1-P5 corrections are substantively satisfied. No new research-scale execution is needed. One remaining regularity statement in T3 must be corrected before manuscript adoption.

## Accepted corrections

1. T1 now separates the global exact coupling from the local/asymptotic moment expansion and states explicit convergence/interchange conditions.
2. The report no longer says the market enters the RL problem only through the scalar wealth map; it also identifies the transition-law effect on histories, occupancy and continuation values.
3. The unsupported bounded-return-support rationale is withdrawn and a domination assumption is stated explicitly.
4. T3.4 correctly treats CRN central finite differences as a numerical approximation with O(h^2) truncation error, not as an unbiased estimator.
5. T4 adopts the symmetric midpoint decomposition under a common dominating measure and retains the S/M reference decompositions only as supporting identities. The decomposition is explicitly described as attribution, not causal identification.

## Remaining correction P6 — score regularity must account for state dependence

The current report states that A3 implies `|psi_theta|` and the direct entropy derivative are uniformly bounded over the parameter neighbourhood and action interval, and therefore reduces A4 to first-moment integrability of terminal log wealth.

That reduction is not justified for the frozen actor parameterisation. The policy-parameter score may be bounded because location/scale are constrained, but the actor score with respect to the linear actor weights contains the state-feature Jacobian. Schematically,

`grad_theta log lambda = grad_phi log lambda * J_transform(raw) * grad_theta raw`,

with `raw = Theta S_t`, so `grad_theta raw` contains `S_t`. Since `S_t` contains `log(W_t/W_0)` and `r_{t-1}`, the actor score and the theta-derivative of entropy need not be uniformly bounded unless the state itself is bounded, which has not been established.

Keep the general domination assumption A4, but delete the claim that it reduces to `E|X_N-X_0| < infinity`. A manuscript-safe sufficient condition is, for finite horizon N,

`E[ (1 + max_t ||S_t||) (1 + |R_soft|) ] < infinity`

uniformly over a local theta-neighbourhood, or an equivalent explicit mixed-moment condition that dominates both the score-weighted soft return and direct entropy derivative. This may be stated as an assumption on the training law; it need not be verified for the frozen SBJTS engine for the theorem to be presented conditionally.

The theorem-to-code map should distinguish `score_phi` from `grad_theta log lambda` and note the chain through the state features.

## What is already manuscript-ready after P6

- exact wealth coupling;
- local moment-entry argument;
- constructive moment-matching non-equivalence;
- trajectory likelihood-ratio policy gradient under history dependence / partial observation, conditional on corrected regularity assumptions;
- symmetric occupancy / continuation-value attribution identity;
- structural lag-return channel result;
- entropy time-scaling distinction;
- theorem-to-code and mutation evidence.

## Execution instruction

Patch only the theory report, unit-check metadata/map if affected, and ticket progress. No training, holdout evaluation, Colab run, or new empirical estimand is authorized.
