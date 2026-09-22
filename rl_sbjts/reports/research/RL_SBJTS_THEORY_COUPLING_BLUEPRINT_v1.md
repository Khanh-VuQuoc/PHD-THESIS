# RL–SBJTS Theory Coupling Blueprint v1

**Date:** 2026-09-22  
**Goal:** convert the now-established empirical mechanism into a rigorous theoretical contribution without changing the frozen learner or market experiment.

## 1. Full market history, observation, action, and wealth

Let \(H_t\) denote the full simulator history/state required by the SBJTS transition law. The learner observes only

\[
S_t=g(H_t,W_t)=\left(1,t/N,\log(W_t/W_0),r_{t-1}\right).
\]

The policy is observation based:

\[
A_t=\pi_t\sim \lambda_\theta(\cdot\mid S_t).
\]

The market transition under law \(L\in\{S,M\}\) is

\[
H_{t+1}\sim Q_L(dh'\mid H_t,A_t),
\]

with the important implementation restriction that \(Q_L\) does not depend directly on actor parameter \(\theta\).

The wealth recursion is

\[
W_{t+1}=W_t\big[(1-A_t)R_t^f+A_t e^{r_t}\big].
\]

Under the primary frozen convention \(R_t^f=1\),

\[
X_{t+1}-X_t
=g(A_t,r_t)
=\log\{1+A_t(e^{r_t}-1)\},
\qquad X_t=\log W_t.
\]

This equation is the exact market-to-RL coupling.

## 2. Proposition A — local moment matching is insufficient

For fixed action \(a\),

\[
g(a,r)=ar+\frac12a(1-a)r^2
+\frac16a(1-a)(1-2a)r^3+O(r^4).
\]

Hence equality of the first two unconditional moments under two return laws does not, in general, imply equality of expected portfolio growth, continuation values, state occupancy, or policy gradient. A sufficient reason is either

\[
E_S[r_t^k]\neq E_M[r_t^k]\quad\text{for some }k\ge3
\]

or

\[
Q_S(r_t\in\cdot\mid H_t)\neq Q_M(r_t\in\cdot\mid H_t)
\]

on a set of positive occupancy probability.

The paper should prove this as a non-equivalence proposition, not as a claim that every pair of moment-matched laws must produce different optimal policies.

## 3. Proposition B — trajectory likelihood-ratio gradient under history dependence

Define the frozen discrete soft objective

\[
J_L(\theta)
=
E_{\theta,L}\left[
X_N-X_0+
m\sum_{t=0}^{N-1}{\cal H}(\lambda_\theta(\cdot\mid S_t))
\right].
\]

For a trajectory \(\tau=(H_0,A_0,\ldots,H_N)\),

\[
p_{\theta,L}(\tau)
=
p_0(H_0)
\prod_{t=0}^{N-1}
\lambda_\theta(A_t\mid S_t)
Q_L(dH_{t+1}\mid H_t,A_t).
\]

If \(Q_L\) is actor-parameter independent and regularity permits differentiation under the integral,

\[
\nabla_\theta\log p_{\theta,L}(\tau)
=
\sum_t\nabla_\theta\log\lambda_\theta(A_t\mid S_t).
\]

Therefore

\[
\nabla_\theta J_L
=
E\left[
R_L^{\rm soft}(\tau)
\sum_t\nabla_\theta\log\lambda_\theta(A_t\mid S_t)
+
m\sum_t \partial_\theta {\cal H}(\lambda_\theta(\cdot\mid S_t))
\right],
\]

where the partial derivative holds the sampled state fixed; visitation effects are already carried by the trajectory score term. A baseline/advantage form follows in the usual way and does not require the observed four-dimensional state itself to be Markov.

The correct formal object is therefore a history-state/POMDP-style process with an observation-based policy, not an unsupported assertion that \(S_t\) is a complete Markov state.

## 4. Proposition C — training-law interaction decomposition

Let \(d_{L,t}^\theta(h)\) be the time-\(t\) occupancy density of full history state under law \(L\), and let \(A_{L,t}^{\theta,\mathrm{soft}}(h,a)\) denote a soft advantage chosen so that the score-function part of the gradient is

\[
G_L^{\rm score}
=
\sum_t\int d_{L,t}^\theta(h)
\lambda_\theta(a\mid g(h))
\psi_\theta(a,g(h))
A_{L,t}^{\theta,\mathrm{soft}}(h,a)\,da\,dh,
\]

with \(\psi_\theta=\nabla_\theta\log\lambda_\theta\).

Then

\[
d_SA_S-d_MA_M=(d_S-d_M)A_S+d_M(A_S-A_M).
\]

Accordingly, the SBJTS-versus-Merton gradient difference has two conceptually distinct channels:

1. **occupancy channel** — the training laws visit different histories/states;
2. **continuation-value channel** — the same local state/action can have a different future value under a different conditional path law.

If the direct entropy derivative is kept outside the soft advantage, there is an additional entropy-occupancy term because the same policy entropy is averaged under different \(d_L\). The manuscript must state which convention it uses.

## 5. Proposition D — why lagged return can matter in SBJTS but not iid GBM

The leading term in the one-step growth expansion is

\[
E[\pi_t r_t]
=
E\left[\pi_\theta(S_t)E(r_t\mid S_t)\right].
\]

Under iid GBM increments,

\[
E_M(r_t\mid S_t)=E_M(r_t)
\]

apart from information already encoded through wealth/action history that does not forecast the next independent innovation. Thus \(r_{t-1}\) has no direct predictive role for the next return law.

Under SBJTS,

\[
E_S(r_t\mid H_t)
\]

may depend on lagged returns and other path information. Since the frozen policy observes \(r_{t-1}\), it can exploit the component of that conditional structure visible through \(S_t\).

The completed experiment is consistent with this mechanism: the saved SBJTS actors have large negative lag-return feedback while Merton actors are nearly flat in that coordinate.

This proposition should be written carefully as a structural channel, not as proof that the specific SBJTS generator's lagged conditional mean alone causes the full performance gain. A dedicated conditional-law diagnostic or ablation would strengthen causal attribution.

## 6. Entropy time scale

The frozen discrete learner uses

\[
J_{\rm disc}=E[X_N-X_0]+m\sum_t H_t.
\]

The continuous-time source paper uses

\[
J_{\rm cont}=E[X_T]+\lambda\int_0^T H_t\,dt.
\]

On a regular grid,

\[
m=\lambda\Delta t.
\]

With \(\Delta t=1/250\) and frozen \(m=0.01\), the continuous-time-equivalent rate is \(\lambda=2.5\). This distinction does not invalidate the direct SBJTS-versus-Merton learned-arm contrast because both arms share the same frozen discrete objective, but it must remain explicit whenever the analytic Merton benchmark is discussed.

## 7. Required proof/code verification

The next theory deliverable should contain:

- formal assumptions for differentiability/integrability/support;
- a proof of the trajectory gradient result without assuming the four-feature observation is Markov;
- the precise soft-advantage convention and entropy term;
- a counterexample or constructive argument for moment-matching insufficiency;
- the occupancy/continuation decomposition;
- a theorem-to-code map: wealth recursion, state map, policy density, entropy, score gradient, critic target, seed-independent environment law;
- unit checks only; no research training.

## 8. Claims not yet justified by theory

Do not claim:

- truncated Gaussian is globally optimal under SBJTS;
- the observed four-feature state is a complete Markov state;
- the direct comparator isolates a pure jump effect;
- lagged return is the sole causal mechanism;
- universal RL–SBJTS superiority.
