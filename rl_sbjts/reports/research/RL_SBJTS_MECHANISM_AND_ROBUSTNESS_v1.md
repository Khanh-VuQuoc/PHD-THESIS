# RL–SBJTS Mechanism and Robustness Update v1

**Date:** 2026-09-22  
**Scope:** scientific interpretation of the completed user-Colab T4 comparator. This is a research result note, not an audit memo.

## 1. Direct comparator result

The direct comparison uses the same learner class, state, action constraints, exploration setting, training budget, and frozen SBJTS target holdout. The intended scientific difference is the training market law: frozen SBJTS versus empirical Merton/GBM.

Recomputation from the raw ledgers yields 24,000 one-to-one TT–MT pairs after removing the single known exact duplicate TT row.

| Constraint | Endpoint | SBJTS mean | Merton mean | SBJTS − Merton |
|---|---:|---:|---:|---:|
| FULL | mean terminal log wealth | 0.01484303 | 0.01263671 | **+0.00220632** |
| FULL | CVaR log loss | 0.08385853 | 0.08703948 | **−0.00318095** |
| CAP50 | mean terminal log wealth | 0.00752284 | 0.00696874 | **+0.00055409** |
| CAP50 | CVaR log loss | 0.04154664 | 0.04230770 | **−0.00076106** |

The frozen crossed-cluster bootstrap in `primary_estimands.json` excludes zero for all four co-primary contrasts. A stricter policy-level sensitivity analysis that first collapses all 300 target-holdout blocks within each trained replication and then bootstraps only the 40 paired training replications also excludes zero for all four outcomes:

| Constraint | Endpoint | policy-level 95% bootstrap CI | favorable replications |
|---|---|---:|---:|
| FULL | wealth | [+0.0021807, +0.0022330] | 40/40 |
| FULL | CVaR loss | [−0.0032170, −0.0031443] | 40/40 |
| CAP50 | wealth | [+0.0005470, +0.0005610] | 40/40 |
| CAP50 | CVaR loss | [−0.0007694, −0.0007525] | 40/40 |

This supports a **domain-scoped training-law advantage**: under the tested SBJTS deployment law, the SBJTS-trained learner has higher terminal log wealth and lower CVaR log loss than the otherwise matched empirical-GBM-trained learner. It does not imply universal superiority.

## 2. The difference is not explained by average risky exposure

Average executed exposure is nearly the same across training arms:

- FULL: SBJTS `0.500677` versus Merton `0.499760`.
- CAP50: SBJTS `0.249915` versus Merton `0.249670`.

Executed action variance is also nearly unchanged. Therefore the performance gap is not well described as a simple leverage/exposure effect.

## 3. Learned feedback rule differs sharply

The actor uses the frozen state

\[
s_t=(1,t/N,\log(W_t/W_0),r_{t-1}),
\]

with two linear raw outputs before the frozen smooth transform to the truncated-Gaussian action law. The mean raw-location coefficients are:

| Arm | Constraint | intercept | time | log wealth | lagged return |
|---|---|---:|---:|---:|---:|
| MERTON | LONG_ONLY_FULL | +0.0328 | −0.0870 | −0.0171 | +0.0327 |
| SBJTS | LONG_ONLY_FULL | +0.0324 | −0.0743 | −0.5534 | −1.5631 |
| MERTON | LONG_ONLY_CAP50 | +0.0330 | −0.0898 | −0.0650 | +0.0292 |
| SBJTS | LONG_ONLY_CAP50 | +0.0331 | −0.0841 | −0.4249 | −1.1698 |

The strongest separation is in the state-feedback coefficients. In FULL, the lag-return coefficient is about −1.56 under SBJTS versus +0.03 under Merton; the log-wealth coefficient is about −0.55 versus −0.02. The CAP50 pattern is qualitatively the same.

## 4. Executed policy-response surface

Because raw coefficients pass through the actual frozen `policy_from_raw_batch` transform and then through a truncated Gaussian, coefficient magnitudes alone are not the final economic object. Each saved policy was propagated through the exact transform and the executed truncated-Gaussian mean action was calculated at a representative mid-horizon state.

At `t/N=0.5`, `log(W/W0)=0`:

| Constraint | lag return | Merton mean action | SBJTS mean action |
|---|---:|---:|---:|
| LONG_ONLY_CAP50 | −0.06 | 0.247499 | 0.262132 |
| LONG_ONLY_CAP50 | −0.03 | 0.247688 | 0.254966 |
| LONG_ONLY_CAP50 | 0.00 | 0.247873 | 0.248373 |
| LONG_ONLY_CAP50 | +0.03 | 0.248054 | 0.242336 |
| LONG_ONLY_CAP50 | +0.06 | 0.248231 | 0.236834 |
| LONG_ONLY_FULL | −0.06 | 0.494688 | 0.542746 |
| LONG_ONLY_FULL | −0.03 | 0.495129 | 0.519239 |
| LONG_ONLY_FULL | 0.00 | 0.495566 | 0.497920 |
| LONG_ONLY_FULL | +0.03 | 0.496000 | 0.478765 |
| LONG_ONLY_FULL | +0.06 | 0.496431 | 0.461685 |

The Merton policy is nearly flat in lagged return. The SBJTS policy is economically state-responsive: after a negative lagged return it raises risky exposure, while after a positive lagged return it lowers exposure.

The local numerical derivative of the executed mean action at the same representative state is:

| Constraint | state coordinate | Merton slope | SBJTS slope |
|---|---|---:|---:|
| LONG_ONLY_FULL | lag return | +0.0145 | −0.6742 |
| LONG_ONLY_FULL | log wealth | −0.0033 | −0.2377 |
| LONG_ONLY_CAP50 | lag return | +0.0061 | −0.2104 |
| LONG_ONLY_CAP50 | log wealth | −0.0095 | −0.0755 |

This is direct mechanism evidence that the two training laws produce different feedback policies, even though their unconditional average risky exposure is almost the same.

## 5. Robustness / negative-control checks

1. **Policy-level clustering sensitivity.** Collapsing the 300 evaluation blocks per training replication and using only 40 paired policy units leaves all four intervals away from zero.
2. **Replication sign consistency.** All 40/40 paired training replications have the favorable sign for both co-primary endpoints in both constraint strata.
3. **Paired sign-flip randomization.** A 100,000-draw policy-level sign-flip randomization gives Monte Carlo two-sided `p ≈ 1e-5` for each of the four contrasts. This is an exploratory robustness diagnostic, not a preregistered confirmatory test.
4. **Identity negative control.** Feeding an arm against its identical copy gives exactly zero contrast by construction. The existing notebook smoke suite separately established fail-closed hardware and inference-gate behavior.

The remaining requested gate-mutation checks for U0–U3 should be implemented as cheap unit tests; they do not require retraining.

## 6. Paper interpretation

The empirical story can now be written as

\[
\boxed{\text{training market law}\rightarrow\text{learned state feedback}\rightarrow\text{different target outcomes}}.
\]

Base 4 already showed that matching local mean/variance does not remove path-level temporal differences. The direct Merton comparator now shows that a learner trained under the richer SBJTS law develops a substantially stronger response to lagged return and current wealth, and that this policy performs better on the SBJTS deployment law.

The next bottleneck is theoretical, not computational: formalize why a history-dependent conditional return law changes the soft RL objective/gradient and separate the **occupancy** and **continuation-value** channels.
