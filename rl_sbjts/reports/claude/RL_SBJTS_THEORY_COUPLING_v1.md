# RL–SBJTS theory coupling and theorem-to-code verification v1

**Ticket:** `C-RLSBJTS-THEORY-COUPLING-01`  
**Status:** `READY_FOR_PMO_THEORY` — derivation, theorem-to-code verification and unit/mutation tests only.  
**Execution class:** `SMOKE_EVIDENCE`. No research-scale training or evaluation was run; no estimand was recomputed; no claim was created or modified.  
**Generated:** 2026-09-22T02:24:58.433008+00:00 · full package runs in 74.8 s on CPU.

**Frozen sources this package is written against**

- Base 3 embedded notebook `344956031d9e8976…`, code-cell concat `db500333b57ae902…` (matches pinned: `True`)
- 17 native AST engine components, 0 mismatches
- market snapshot `7e817762849118fc…`, training slice `09811db465da1443…` (matches pinned: `True`), environment fingerprint `63ba37cc4a26b48b…`

Everything below is either exact algebra, exact finite enumeration, Gauss–Legendre quadrature on the frozen density, source inspection of the frozen code text, or execution of the frozen project's own mathematics suite. Where the frozen source already carries a verification of an object, that frozen test is **executed** rather than replaced.

---

## T1 — exact wealth coupling

The frozen wealth recursion is

$$ W_{t+1}=W_t\big[(1-A_t)R^f_t+A_te^{r_t}\big], $$

and under the Base 4 primary convention $R^f_t=1$, with $X_t=\log W_t$,

$$ X_{t+1}-X_t=g(A_t,r_t)=\log\{1+A_t(e^{r_t}-1)\}. $$

This is the exact market-to-RL coupling: the market enters the learning problem only through this scalar map.

### T1.1 Third-order expansion

Writing $u=e^r-1=r+\tfrac12r^2+\tfrac16r^3+O(r^4)$ and expanding $\log(1+au)$,

$$ g(a,r)=ar+\tfrac12a(1-a)r^2+\tfrac16a(1-a)(1-2a)r^3+O(r^4). $$

Verified symbolically against the frozen expression, coefficient by coefficient:

| order | derived | claimed | identical |
|---|---|---|---|
| 1 | `a` | `a` | True |
| 2 | `-a**2/2 + a/2` | `-a**2/2 + a/2` | True |
| 3 | `a**3/3 - a**2/2 + a/6` | `a**3/3 - a**2/2 + a/6` | True |

The truncation error scales as $r^4$: halving $r$ divides the maximum error by 15.99, 16.00, 16.00.

### T1.2 Which return features can enter expected growth

The action is drawn from $\lambda_\theta(\cdot\mid S_t)$ and is conditionally independent of the contemporaneous return given the history state, so each expansion term factorises into an action polynomial moment times a **conditional** return moment:

$$ E[X_{t+1}-X_t]=\sum_{k\ge1}E\big[c_k(A_t)\,E(r_t^k\mid H_t)\big]. $$

| $k$ | $c_k(a)$ | action moments required | multiplies |
|---|---|---|---|
| 1 | `a` | [1] | `E[ r_t^1 \| H_t ]` |
| 2 | `-a**2/2 + a/2` | [1, 2] | `E[ r_t^2 \| H_t ]` |
| 3 | `a**3/3 - a**2/2 + a/6` | [1, 2, 3] | `E[ r_t^3 \| H_t ]` |
| 4 | `-a**4/4 + a**3/2 - 7*a**2/24 + a/24` | [1, 2, 3, 4] | `E[ r_t^4 \| H_t ]` |

Two consequences matter for the comparator. First, expected growth depends on **conditional** return moments of every order, not on the unconditional mean and variance alone. Second, because $c_2(a)=\tfrac12a(1-a)$ is not affine in $a$, the **exploration variance of the action enters expected growth at second order**: two policies with the same mean action but different dispersion have different expected growth. That is the precise sense in which the frozen entropy-regularised objective is coupled to the market law rather than merely regularised.

## T2 — local moment matching does not imply RL equivalence

**Proposition.** There exist pairs of return laws with identical unconditional one-step mean and variance at every $t$ for which the expected-growth functional, the optimal observation-based policy and the policy gradient all differ. Equality of the first two unconditional one-step moments is therefore not sufficient for RL equivalence.

This is an **existence** statement. It does not say that every moment-matched pair must induce different policies: two laws equal as processes trivially induce the same policy. Two independent mechanisms are exhibited.

### T2a Higher unconditional moments (iid, no path dependence)

Law A is the symmetric two-point law on $\{-\delta,+\delta\}$; law B is a three-point law on $\{-2\delta,0,\delta\}$ with probabilities $(\tfrac16,\tfrac12,\tfrac13)$. Both have mean 0 and variance $\delta^2$ exactly (observed gaps 0.0e+00 and 2.7e-20); their third central moments differ by 2.248e-06.

For any symmetric two-point law the growth-optimal constant action is exactly $\tfrac12$: with $p=e^\delta-1$, $q=e^{-\delta}-1$ one has $a^\star=-(p+q)/(2pq)$, and since $p+q=2(\cosh\delta-1)$ while $pq=-2(\cosh\delta-1)$, $a^\star=\tfrac12$ for every $\delta$. Root-finding on the exact derivative returns 0.499999999999997 for law A (matches the analytic value: True) and 0.501091651055189 for law B, a gap of 1.092e-03 at the study's own per-step scale $\delta=0.0131$.

The magnitudes obey the scaling T1 predicts, which is a three-way consistency check rather than a separate claim:

| quantity | predicted order in $\delta$ | observed order |
|---|---|---|
| shift in the optimal action | 1 | 1.000 |
| growth gap at $a=\tfrac14$ | 3 | 3.004 |
| growth gap at $a=\tfrac12$ | 4 | 3.998 |

The fourth-order behaviour at $a=\tfrac12$ is not an anomaly: c_3(a) = a(1-a)(1-2a)/6 vanishes at a = 1/2, which is exactly law A's optimum, so the third-order contribution to the gap is zero there and the leading difference is fourth order. At a = 1/4, where c_3 != 0, the gap is third order. Both are consistency checks on the T1 expansion.

### T2b Conditional/path law, with *identical* one-step marginals

The stronger construction matches not merely two moments but the **entire** one-step marginal at every $t$. Returns are $\pm\delta$ with probability $\tfrac12$ under both laws; law $M$ has $r_1$ independent of $r_0$, law $S$ has $r_1=-r_0$. Every unconditional one-step moment of every order therefore agrees, and only the conditional law differs.

Because the frozen observation carries $r_{t-1}$, take the policy affine in the lagged return through the frozen raw-to-policy transform and differentiate the exact two-step objective with respect to the lag coefficient at zero:

| law | $\partial J/\partial b_{\text{lag}}$ at $b_{\text{lag}}=0$ | $\arg\max_{b_{\text{lag}}}J$ | objective range over the lag grid |
|---|---|---|---|
| M | **0 (exactly)** | **0 (exactly)** | 7.419e-04 |
| S | -0.0108747 | -200 (grid boundary) | 7.868e-02 |

Under the iid law the derivative is **exactly zero** and the exact maximiser is **exactly zero**; under the conditionally dependent law the derivative is -0.01087 and the objective is 106× more sensitive to the lag coefficient. Two honest caveats: under $S$ the maximiser sits at the boundary of the searched grid, because as $|b_{\text{lag}}|$ grows the policy approaches a bang-bang limit, so the sign and the exact-zero contrast are the content here, not the magnitude; and the objective under $M$ is not *flat* in the lag coefficient either — a non-zero lag coefficient under the iid law adds action dispersion with no first-order return benefit, and the order-2 term a(1-a)/2 * E[r^2] is not affine in a, so it is a pure cost; the derivative at zero is exactly zero and zero is the exact maximiser.

**This is the theoretical counterpart of the observed policies.** The measured Merton actor has a lagged-return coefficient of about $+0.03$, i.e. indistinguishable from the exactly-zero optimum this model predicts for an iid training law, while the measured SBJTS actor has about $-1.56$. The theory predicts the qualitative pattern that the mechanism report found.

## T3 — trajectory policy gradient under history dependence and partial observation

Let $H_t$ be the full simulator history state, $S_t=g(H_t,W_t)=(1,t/N,\log(W_t/W_0),r_{t-1})$ the learner observation, and $A_t\sim\lambda_\theta(\cdot\mid S_t)$. For a trajectory $\tau=(H_0,A_0,\dots,H_N)$,

$$ p_{\theta,L}(\tau)=p_0(H_0)\prod_{t=0}^{N-1}\lambda_\theta(A_t\mid S_t)\,Q_L(dH_{t+1}\mid H_t,A_t). $$

### Assumptions

- **(A1) actor-parameter independence of the market kernel.** $Q_L$ does not depend on $\theta$. Verified in code, not assumed: see T3.5.
- **(A2)** the initial law $p_0$ does not depend on $\theta$.
- **(A3) strict positivity and smoothness.** $\lambda_\theta(a\mid s)>0$ on the open interval $(\text{lo},\text{hi})$ and is $C^1$ in $\theta$. The frozen policy is a truncated Gaussian whose scale is confined to $[\text{scale\_floor},\text{scale\_ceiling}]$ by construction and whose location is confined to a finite box, so the density is bounded away from zero on compacts.
- **(A4) interchange of $\nabla_\theta$ and $E$.** The action set is compact, the returns are bounded on the simulated support, and the raw-to-policy transform is smooth and bounded, so the integrand and its $\theta$-derivative are dominated locally uniformly in $\theta$.

**$S_t$ is nowhere assumed to be a Markov state.** The correct object is a history-state process with an observation-based policy; the derivation uses only that the policy is $S_t$-measurable and that $Q_L$ is $\theta$-free.

### Result

Under (A1)–(A2), $\log p_{\theta,L}(\tau)=\log p_0+\sum_t\log\lambda_\theta(A_t\mid S_t)+\sum_t\log Q_L(\cdot)$ and the last sum is $\theta$-free, so

$$ \nabla_\theta\log p_{\theta,L}(\tau)=\sum_t\nabla_\theta\log\lambda_\theta(A_t\mid S_t)\;=:\;\sum_t\psi_\theta(A_t,S_t). $$

The frozen objective carries a $\theta$-dependent integrand, so the product rule gives two terms:

$$ J_L(\theta)=E\Big[X_N-X_0+m\sum_t\mathcal H(\lambda_\theta(\cdot\mid S_t))\Big], $$
$$ \nabla_\theta J_L=\underbrace{E\Big[R^{\rm soft}(\tau)\sum_t\psi_t\Big]}_{\text{trajectory score}}+\underbrace{m\,E\Big[\sum_t\partial_\theta\mathcal H(\lambda_\theta(\cdot\mid S_t))\Big]}_{\text{direct entropy derivative, state held fixed}}. $$

Occupancy effects are carried entirely by the first term; the second is a partial derivative at fixed sampled state. This is exactly the split the frozen `actor_gradient` implements as `score * advantage + m * entropy_gradient`.

### Why the frozen return-to-go excludes $\mathcal H_t$

The lemma everything rests on is $E[\psi_t\mid S_t]=0$, which holds because $\int\lambda\nabla_\theta\log\lambda\,da=\nabla_\theta\int\lambda\,da=0$. Hence any $S_t$-measurable factor multiplying $\psi_t$ contributes nothing. $\mathcal H_t$ is a deterministic function of $S_t$ and $\theta$ and does not depend on $A_t$, so $E[\psi_t\,m\mathcal H_t]=0$ and it may be dropped from the return-to-go. The frozen

$$ G_t=\sum_{u\ge t}\Delta_u+m\sum_{u>t}\mathcal H_u $$

is therefore not an arbitrary convention: it removes a provably zero-expectation term and avoids double-counting against the analytic entropy gradient. The same lemma gives baseline invariance for the critic.

### Verification

| check | what it establishes | observed | tolerance | pass |
|---|---|---|---|---|
| T3.1 $E[\psi\mid S]=0$ | the lemma, on 38 frozen resolvable test regimes by quadrature | 2.2e-12 | 1e-08 | True |
| T3.2 baseline invariance | $E[\psi\,b(S)\mid S]=0$ for arbitrary $b$ | 3.2e-11 | 1e-06 | True |
| T3.3 entropy convention | frozen `soft_return_to_go` equals $\sum_{u\ge t}\Delta_u+m\sum_{u>t}\mathcal H_u$ | 2.1e-17 | 1e-12 | True |
| T3.4 score vs pathwise | the whole gradient identity, end to end | max $\|z\|$ = 1.59 | 4$\sigma$ | True |
| T3.5 $\nabla_\theta\log Q_L=0$ | (A1), in code | see below | exact | True |

T3.3 is not vacuous: the two conventions differ numerically by 0.0145 on the fixture, yet both give the same gradient in expectation.

T3.4 is the strongest check in the package. With inverse-CDF sampling from a **fixed** uniform block the action is a smooth reparameterisation of $\theta$, so the central difference of the per-path objective is an unbiased *pathwise* estimator of $\nabla_\theta J$ — and because the state path itself moves with $\theta$ under common random numbers, it includes the occupancy effect. The score-function estimator is a different unbiased estimator of the same quantity. On 200,000 paths at 6 steps the two agree to a worst paired $z$ of 1.59, and the frozen `actor_gradient` reproduces the replicated contraction to 7.8e-15.

One honest qualification on the critic. The frozen critic is refit on the same batch that supplies the actions, so the fitted baseline is not exactly action-independent and the baselined estimator is not guaranteed unbiased at finite sample. Measured against the provably unbiased unbaselined estimator the baselined gradient sits 0.54 standard errors away, i.e. within noise at this sample size. This is a variance-reduction device, not part of the theorem.

T3.5 verifies (A1) three ways: the market block is byte-identical across repeated construction; the market batch is built **before** the actor acts in the frozen training body; and the market seed expression is `env_root * 1000 + it`, which contains no actor state. The frozen engine signature takes no actor argument.

## T4 — occupancy and continuation-value channels

Let $d^\theta_{L,t}(h)$ be the time-$t$ occupancy of the full history state under law $L$, and let $A^{\theta,\rm soft}_{L,t}(h,a)=Q^{\rm soft}_{L,t}(h,a)-V^{\rm soft}_{L,t}(h)$ with the frozen $u>t$ entropy convention. Then the score part of the gradient is

$$ G^{\rm score}_L=\sum_t\int d^\theta_{L,t}(h)\int\lambda_\theta(a\mid g(h))\,\psi_\theta(a,g(h))\,A^{\theta,\rm soft}_{L,t}(h,a)\,da\,dh, $$

and the training-law gradient gap splits as

$$ d_SA_S-d_MA_M=\underbrace{(d_S-d_M)A_S}_{\text{occupancy channel}}+\underbrace{d_M(A_S-A_M)}_{\text{continuation-value channel}}. $$

### Verification on an exactly enumerable model

Three decisions, returns $\pm\delta$, 21 quadrature action nodes, law $M$ iid and law $S$ the mirror chain $r_t=-r_{t-1}$. All one-step marginals agree at every $t$. With two decisions the two laws cannot differ in occupancy at any decision time and the occupancy channel is zero for trivial reasons.

- **Representation check.** The occupancy-times-advantage form equals brute-force trajectory enumeration to 6.9e-12. This is what licenses the decomposition at all.
- **Occupancy genuinely differs.** Identical at $t=1$ (`True`) and total variation 0.50 at $t=2$.

| split | occupancy channel | continuation-value channel | residual vs total |
|---|---|---|---|
| advantage referenced at $S$ | -1.456732e-04 | -4.373597e-04 | 0.0e+00 |
| advantage referenced at $M$ | +0.000000e+00 | -5.830329e-04 | 0.0e+00 |
| total gap | — | — | -5.830329e-04 |

### A finding the manuscript must carry: the split is not unique

Both identities are exact and both sum to the total, but they attribute the interaction term differently. In this model the occupancy channel is -1.457e-04 when the advantage is referenced at $S$ and **exactly zero** when it is referenced at $M$ — a disagreement of 1.457e-04, which is about a quarter of the total gap. A channel magnitude is not split invariant, so the manuscript must state which law the advantage is referenced at; only the total is convention free.

### The entropy channel is purely occupancy

With the direct entropy derivative kept outside the soft advantage, its contribution to the law gap is $m\sum_t\int(d_{S,t}-d_{M,t})\,\partial_\theta\mathcal H\,dh$: the same $\partial_\theta\mathcal H$ averaged under two different occupancy measures. In this model that term is 0.0e+00, and it vanishes for a specific and instructive reason — the design matches every one-step marginal, and $\partial_\theta\mathcal H$ depends on the history only through $r_{t-1}$, whose marginal is matched by construction. With unmatched marginals it would not vanish, so the manuscript should state the convention rather than omit the term.

## T5 — structural role of the lagged return

Because $A_t$ is conditionally independent of $r_t$ given $H_t$ and the policy is $S_t$-measurable, the leading growth term factorises:

$$ E[A_tr_t]=E\big[\bar\pi_\theta(S_t)\,\mu_L(H_t)\big]=E[\bar\pi]\,E[\mu_L]+\operatorname{Cov}\big(\bar\pi_\theta(S_t),\mu_L(H_t)\big),\qquad \mu_L(H_t)=E_L(r_t\mid H_t). $$

Under an iid law $\mu_M$ is a **constant**, so the covariance term is identically zero for *every* observation-based policy and the lagged-return coordinate has no first-order effect on expected growth beyond what the intercept already controls. Under a history-dependent law $\mu_S$ is state dependent and the covariance term is available to be exploited. Exactly, on the enumerable model:

| law | $\operatorname{Cov}(\bar\pi,\mu_L)$ | $E[\bar\pi\,\mu_L]$ | $E[\bar\pi]E[\mu_L]$ |
|---|---|---|---|
| M | +0.000000e+00 | +0.000000e+00 | +0.000000e+00 |
| S | +5.833244e-04 | +5.833244e-04 | +0.000000e+00 |

Under $S$ the entire first-order growth benefit **is** the covariance term. The channel is present under one law and provably absent under the other.

### The frozen SBJTS engine is history dependent by construction

This is established by source inspection of the frozen engine, not by a statistical test:

- `carries_forward_the_position_state_Y`: True
- `accumulates_a_path_kernel_weight_logw`: True
- `jump_intensity_built_from_those_accumulated_weights`: True
- `jump_class_conditioning_uses_the_accumulated_weights`: True
- `bridge_drift_depends_on_the_current_position`: True

The load-bearing lines are:

```python
logw = logw - np.log(np.clip(quartic_kernel_np(dold,h),1e-30,None))
logw = logw + np.log(np.clip(quartic_kernel_np(dcur,h),1e-30,None))
ell = np.clip(prob_scale*ell_raw, 0.0, 1.0)
lwe = np.where(pop, logw, -1e30)
lwe = np.where(empty[:,None], logw, lwe)
lwe = logw
Y = Y + drift*dt_sub + BM[:,bmi,:]*sig*math.sqrt(dt_sub)
```

`logw` accumulates a path functional of kernel weights across steps; the Bernoulli jump intensity `ell` is built from it; the jump-class conditioning `lwe` uses it; and the position state `Y` is carried forward into the bridge drift. By contrast the comparator's Merton arm draws `m1 + sd * standard_normal` independently per path and step, so $E(r_t\mid H_t)=m_1$ identically.

### What this does not establish

This establishes that the lagged-return channel EXISTS under a history-dependent law and CANNOT exist under an iid law. It does not measure the frozen SBJTS conditional mean function, and it does not establish that the lagged-return channel accounts for any particular share of the observed performance gap. Occupancy, continuation-value, wealth-state and higher-moment channels remain unseparated.

## Entropy time-scaling discipline

The frozen discrete objective and the Chau–Nguyen–Nguyen continuous-time objective are

$$ J_{\rm disc}=E[X_N-X_0]+m\sum_tH_t,\qquad J_{\rm cont}=E[X_T]+\lambda\int_0^TH_t\,dt, $$

and they coincide on the frozen grid iff $m=\lambda\,\Delta t$. At $\Delta t=1/250$ the frozen $m=0.01$ is $\lambda=2.5$, while the paper's nominal $\lambda=0.01$ is $m=4e-05$ — a factor of 250.

Carried forward from the comparator package and re-executed here: **`ENTROPY_TIME_SCALING_TESTS_PASS`**. The three tests are the sum identity, grid invariance (refining the grid leaves the optimum unchanged iff $m$ is rescaled, and moves it if $m$ is held fixed) and scale separation (identifying $m$ with $\lambda$ moves the optimum materially).

This does not affect the learned-arm contrast, because both arms optimise the same frozen discrete objective at the same $m$, so the factor is common and cancels. It decides exactly one thing: which exploration weight the analytic Merton benchmark is built at. Every analytic-Merton reference must state the convention.

## Theorem-to-code verification map

Machine-readable copy: `evidence/theory_coupling_v1/theorem_code_map.csv`.

| mathematical object | frozen implementation | verification | observed | pass |
|---|---|---|---|---|
| T1 wealth coupling  X_{t+1}-X_t = log(1+A(e^r-1)) | `rollout_states_actions / wealth_engine` | exact per-step identity and agreement with the frozen wealth engine | identity 3.9e-16 | True |
| T1 third-order expansion coefficients | `sympy series of the same expression` | symbolic coefficient identity plus O(r^4) remainder scaling | coefficients identical; remainder ratio ~16 | True |
| state map  S_t=(1,t/N,log(W_t/W_0),r_{t-1}) | `state_features + rollout timing` | feature-by-feature check and the r_{-1}=0 / lag-update-after-action contract | all four features and both conventions verified | True |
| truncated-Gaussian density and normalisation | `TruncatedGaussian / TruncatedGaussianBatch` | frozen run_policy_math_tests: logZ/mean/var/entropy/log-prob/scipy/mass | worst scalar-batch 5.4e-10 | True |
| raw-to-policy smooth bounded transform and its Jacobian | `policy_from_raw_batch` | frozen evidence_transform_jacobian: analytic Jacobian vs finite difference | max 4.8e-08 | True |
| policy entropy and its analytic gradient | `TruncatedGaussianBatch.entropy / entropy_gradient_batch` | frozen run_policy_math_tests entropy and entropy-gradient columns | rel 8.0e-07 | True |
| T3 soft return-to-go  G_t = sum_{u>=t} D_u + m sum_{u>t} H_u | `soft_return_to_go` | exact match to the stated formula; H_t dropped because its score is zero | err 2.1e-17 | True |
| critic target and value fit (baseline) | `fit_linear_critic / critic_values` | baseline invariance E[psi b(S)\|S]=0 and rank/condition reporting | max 3.2e-11 | True |
| T3 score  psi = grad_theta log lambda ; E[psi\|S]=0 | `TruncatedGaussianBatch.score_phi` | quadrature over the frozen density on frozen test regimes | max 2.2e-12 | True |
| T3 gradient estimator and its sign | `actor_gradient (+ frozen actor_estimator_toy_test)` | frozen toy test against an analytic target, and score vs pathwise reparameterisation gradient of the frozen objective | toy z<= 4.0; score-vs-pathwise max\|z\| 1.59 | True |
| T3 actor-parameter independence of the market kernel | `market batch construction precedes the actor` | byte-identical market block across constructions; no actor argument; seed schedule free of actor state | grad_theta log Q_L = 0 | True |
| T4 occupancy x soft-advantage representation of the gradient | `derivation, verified on an exactly enumerable model` | brute-force trajectory enumeration vs occupancy/advantage form | max gap 6.9e-12 | True |
| T4 two-channel split and its non-uniqueness | `derivation` | both reference conventions sum to the total exactly; channels disagree | occupancy channel differs by 1.5e-04 between conventions | True |
| T5 lagged-return covariance channel | `derivation + frozen engine source structure` | Cov(pibar, mu_L) exactly zero under iid, non-zero under the conditional law; frozen engine carries path functionals | channel present under S, provably absent under M | True |
| entropy time scaling  m = lambda * dt | `soft_return_to_go vs the continuous-time objective` | sum identity, grid invariance and scale separation | lambda equivalent of frozen m = 2.5 | True |
| seed namespaces; no hidden wall-clock seeding | `seed_of / rng_of` | source scan for global/temporal seeding; hash-derived generators only | forbidden patterns 0 | True |

### Frozen mathematics suite, executed

`run_policy_math_tests` over 144 frozen test regimes, 118 of them numerically resolvable (the frozen code excludes deep-truncation corners from its own gate, and so does this report):

| frozen check | observed | frozen tolerance | pass |
|---|---|---|---|
| `scalar_vs_batch_equivalence` | 5.449e-10 | 1e-08 | True |
| `analytic_score_vs_finite_difference` | 2.370e-06 | 1e-04 | True |
| `entropy_gradient_relative` | 8.044e-07 | 1e-03 | True |
| `density_normalisation` | 1.623e-05 | 1e-03 | True |

`actor_estimator_toy_test` feeds reward $=a$ through the same score machinery the learner uses and compares with the analytic truncated-Gaussian mean derivative:

| $m$ | max $\|z\|$ | sign agreement | non-zero estimate | pass |
|---|---|---|---|---|
| 1.0 | 1.91 | True | True | True |
| 0.1 | 1.52 | True | True | True |
| 0.01 | 1.86 | True | True | True |

`evidence_transform_jacobian` over 6 configurations: worst analytic-vs-finite-difference error 4.78e-08 against the frozen tolerance 1e-06.

### Seeding

Source scan of the frozen code text for global or wall-clock seeding: 0 occurrences across 5 forbidden patterns (`np.random.seed`, `random.seed`, time-derived seeds, global `np.random` draws). Generators are hash-derived from `BASE3_SEED_ROOT = 20260801` over the namespaces ['EVAL_ENV', 'LEARNER', 'ORACLE_ENV', 'TRAIN_ENV', 'VERIFY_ENV'], never from global state.

## Gate-mutation controls

**20/20 controls pass**, of which 14 are negative controls that must fail and do. Each gate is shown to pass on an honest fixture and to fail on a targeted corruption; a gate that cannot be made to fail is not a gate.

| gate | control | expected | observed | pass |
|---|---|---|---|---|
| U0 | `U0_BASELINE_HONEST_SOURCES` | PASS | `PASS` | True |
| U0 | `U0_M1_NOTEBOOK_SINGLE_BYTE_FLIP` | FAIL | `FROZEN_MEMBER_SHA256_MISMATCH` | True |
| U0 | `U0_M2_SNAPSHOT_SINGLE_BYTE_FLIP` | FAIL | `SNAPSHOT_SHA256_MISMATCH` | True |
| U0 | `U0_M3_FROZEN_ENGINE_CONSTANT_EDIT` | FAIL | `FROZEN_MEMBER_SHA256_MISMATCH` | True |
| U0 | `U0_M4_TRAINING_SLICE_REPLACED_BY_VALIDATION_WINDOW` | FAIL | `TRAIN_SLICE_SHA256_MISMATCH` | True |
| U1 | `U1_BASELINE_HONEST_LEDGER` | PASS | `BASE4_TARGET_REPRODUCTION_PASS_WITHIN_FROZEN_BACKEND_TOLERANCE` | True |
| U1 | `U1_M1_ENDPOINT_PERTURBED_BY_1e-3` | FAIL | `BLOCKED_REPRODUCTION` | True |
| U1 | `U1_M2_ATTEMPT_ID_CORRUPTED` | FAIL | `BLOCKED_REPRODUCTION_ATTEMPT_ID_MISMATCH` | True |
| U1 | `U1_M3_REFERENCE_ROW_DELETED` | FAIL | `BLOCKED_REPRODUCTION_REFERENCE_ROWS_MISSING` | True |
| U1 | `U1_M4_SUBSET_OVERRIDE_REFUSED_IN_RESEARCH` | FAIL | `REPRODUCTION_SUBSET_OVERRIDE_FORBIDDEN_OUTSIDE_SMOKE` | True |
| U2 | `U2_BASELINE_RECOVERS_KNOWN_SYNTHETIC_MOMENTS` | PASS | `PASS` | True |
| U2 | `U2_BASELINE_MONTE_CARLO_MOMENT_TEST` | PASS | `PASS` | True |
| U2 | `U2_M1_SIMULATOR_VARIANCE_INFLATED_2_PERCENT` | FAIL | `FAIL` | True |
| U2 | `U2_M2a_MEAN_SHIFTED_BY_HALF_THE_DETECTION_BAND` | PASS | `PASS` | True |
| U2 | `U2_M2b_MEAN_SHIFTED_BY_THREE_TIMES_THE_DETECTION_BAND` | FAIL | `FAIL` | True |
| U2 | `U2_M3_SEED_NAMESPACE_COLLIDES_WITH_A_FROZEN_NAMESPACE` | FAIL | `FAIL` | True |
| U3 | `U3_BASELINE_TINY_POSITIVE_CONTROL` | PASS | `LEARNER_POSITIVE_CONTROL_PASS` | True |
| U3 | `U3_M1_GRADIENT_SIGN_FLIPPED` | FAIL | `LEARNER_POSITIVE_CONTROL_FAIL` | True |
| U3 | `U3_M2_GRADIENT_ZEROED` | FAIL | `LEARNER_POSITIVE_CONTROL_FAIL` | True |
| U3 | `U3_M3_NON_FINITE_WEALTH_INJECTED` | FAIL | `LEARNER_POSITIVE_CONTROL_FAIL` | True |

Two of these deserve comment.

**The calibration gate has a computable detection floor, not a magic threshold.** Its mean band is $4\sqrt{v_1/n}$, equal to 8.069e-05 at the fixture's sample size. A mean shift of half the band correctly does **not** trip it ($z=2.36$) and a shift of three times the band correctly does ($z=12.36$). Both directions are controlled, so the gate is neither blind nor hypersensitive.

**The U1 baseline is the SMOKE-only mechanism subset, not the predeclared two-holdout gate.** The predeclared gate cannot pass in this sandbox: only the first 1 MiB of the 31 MB frozen ledger is retrievable here, so holdout stream 1 has no reference rows. The controls therefore establish that a gate which passes on honest rows fails on corrupted ones. The predeclared gate itself was executed by the user on the Colab T4 and returned `BASE4_TARGET_REPRODUCTION_PASS_EXACT` on all 16 rows; that run is the gate of record, not this fixture.

## Claim discipline

This package creates no new empirical claim and modifies none. Specifically it does **not** claim:

- that the truncated Gaussian is globally optimal under SBJTS — nothing here addresses optimality of the policy class;
- that the four-feature observation is a complete Markov state — T3 is proved *without* that assumption, which is the point of stating it as a history-state problem with an observation-based policy;
- that the comparator isolates a pure jump effect — T2 shows the two laws differ in higher moments *and* conditional structure, and T4 shows at least two distinct gradient channels that the experiment does not separate;
- that lagged return alone causes the performance gain — T5 establishes that the channel exists under $S$ and cannot exist under $M$, which is a structural availability result, not an attribution;
- universal superiority of RL–SBJTS.

The accepted empirical claim remains the domain-scoped statement of `CL-RL-006`: under the tested frozen SBJTS deployment law, the SBJTS-trained learner achieved higher terminal log wealth and lower CVaR log loss than the matched empirical-GBM-trained learner in both frozen constraint strata.

## Unresolved theory issues for PMO

1. **The channel decomposition is not split-invariant.** Demonstrated above: the occupancy channel is about a quarter of the total gap under one reference convention and exactly zero under the other. PMO should decide which convention the manuscript adopts, and the text must report that only the total is convention free. This is a presentation decision with mathematical content, not a defect.
2. **The conditional-law diagnostic is specified but not executed.** T5 is a structural result. Closing the attribution needs the estimand named in `unit_checks.json`: the frozen conditional mean $\mu_S(r_{\rm prev})=E_S(r_t\mid r_{t-1})$, and a lag-ablation contrast obtained by retraining with the $r_{t-1}$ coordinate zeroed out of the frozen state. Both exceed unit scale, and `00_CURRENT_STATE` reserves that decision for PMO, so it is specified rather than run. **`SCOPE CHANGE REQUEST — PMO DECISION REQUIRED`.**
3. **The fitted critic is not part of the theorem.** The frozen critic is refit on the same batch that supplies the actions, so the baselined estimator is not provably unbiased at finite sample. Measured deviation from the unbiased unbaselined estimator is 0.54 standard errors, i.e. within noise here. The manuscript should present the critic as a variance-reduction device and not lean on it in the gradient statement.
4. **T2b's maximiser under the dependent law is unbounded in the searched range.** The exact-zero-versus-nonzero contrast at $b_{\rm lag}=0$ is the rigorous content; the magnitude of the optimal lag coefficient is not, because the objective is monotone in $|b_{\rm lag}|$ toward a bang-bang limit over the range searched. The text should use the derivative statement, not an optimal-coefficient figure.
5. **T1's expansion is a local statement.** It is an $r\to0$ expansion with a verified $O(r^4)$ remainder. The frozen SBJTS law has jumps, so on jump steps the increment is not small and the expansion is not the right tool there; the exact coupling $g(A_t,r_t)$ remains valid without expansion, and the manuscript should use the expansion only for the moment-entry argument.

## Files

- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md` (this file)
- `evidence/theory_coupling_v1/unit_checks.json` — every check, its inputs, its tolerance and its outcome
- `evidence/theory_coupling_v1/theorem_code_map.csv` — the map above, machine readable

All 18 check groups pass; the package runs in 74.8 s on CPU with no research-scale execution.
