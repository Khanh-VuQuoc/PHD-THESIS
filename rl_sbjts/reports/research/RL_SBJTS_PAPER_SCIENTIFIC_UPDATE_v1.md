# RL–SBJTS — Scientific Results Update and Paper-Lock Narrative v1

**Date:** 2026-09-21  
**Purpose:** consolidate the scientific story, quantitative findings, contribution claims, limitations, and remaining theory/mechanism work needed to turn the RL–SBJTS project into a complete manuscript.  
**This document is a research synthesis, not an audit report.**

## 1. Paper-level research question

The paper should be organised around one direct question:

> **What is lost when exploratory portfolio RL is trained under the classical Merton/GBM diffusion law when the deployment market exhibits SBJTS-type jump and temporal dependence, and can training under the richer SBJTS law improve the learned portfolio policy?**

The contribution is therefore not simply “replace a simulator.” The scientific object is the interaction between the **training market law** and the **learned decision rule**.

The target narrative is:

\[
\boxed{
\text{market conditional law}
\rightarrow
\text{RL state/return distribution}
\rightarrow
\text{policy-gradient problem}
\rightarrow
\text{learned feedback rule}
\rightarrow
\text{wealth and tail-risk outcomes}
}
\]

The paper extends the exploratory-Merton RL framework from an idealised diffusion environment to a history-dependent SBJTS environment while holding the RL learner class fixed.

---

## 2. Core scientific thesis now supported by the experiments

The empirical evidence now supports the following narrow thesis:

> **Policies trained under the SBJTS target law and policies trained under an empirically calibrated Merton/GBM law, despite using the same RL learner, action constraints, exploration setting and training budget, produce materially different target-holdout portfolio outcomes. In the tested SBJTS target environment, SBJTS-trained policies have higher terminal log wealth and lower CVaR log loss than Merton/GBM-trained policies.**

This is a **training-law / model-misspecification result**. It is not a statement that Merton is mathematically wrong under its own assumptions, and it is not a universal dominance claim over all markets or RL architectures.

The result complements the earlier Base 4 finding that even after approximately matching canonical one-step mean and variance, the target SBJTS law and a corrected no-jump control remain different in their temporal dependence and lead to different learned-policy outcomes.

Together, the two experiments create a coherent story:

1. **Local first-two-moment matching is not enough to match the path law.**
2. **The remaining temporal dependence is economically relevant to RL training.**
3. **A classical Merton/GBM training law misses this conditional structure.**
4. **Training under SBJTS changes the policy learned by the same RL algorithm and improves target-environment outcomes in the tested setting.**

---

## 3. Model comparison that should anchor the paper

### 3.1 RL–SBJTS arm

The frozen target-trained policies are those from Base 4. The learner uses:

\[
s_t=\left(1,\frac{t}{N},\log\frac{W_t}{W_0},r_{t-1}\right),
\]

with a linear actor, truncated-Gaussian stochastic action policy, linear ridge critic, Adam updates, and hard long-only action bounds.

The wealth transition is

\[
W_{t+1}
=
W_t\left[(1-\pi_t)R_t^f+\pi_t e^{r_t}\right],
\]

and under the primary convention \(R_t^f=1\),

\[
\Delta \log W_t
=
\log\left[1+\pi_t(e^{r_t}-1)\right].
\]

The SBJTS law supplies the conditional distribution of \(r_t\) through its bridge, diffusion and jump channels.

### 3.2 RL–Merton/GBM arm

The direct comparator uses exactly the same RL learner but replaces the training market law by a one-asset empirical GBM calibrated only from the frozen training slice.

The calibration uses the same equally weighted risky log increment consumed by the learner. With \(\Delta t=1/250\),

\[
\sigma_M^2=\frac{v_1}{\Delta t},
\qquad
\mu_M-r_f=\frac{m_1}{\Delta t}+\frac12\sigma_M^2.
\]

The realised research calibration is:

\[
m_1=2.7942696\times10^{-4},
\]

\[
v_1=1.7267919\times10^{-4},
\]

\[
\boxed{\sigma_M=0.2077734},
\qquad
\boxed{\mu_M-r_f=0.0914416}.
\]

The calibration uses 2,110 observations from 2012-01-04 through 2020-05-22 across ITA, XLE, SMH and EUFN, with no validation or target-holdout rows used and no parameter search.

This design isolates the effect of **training under a different market law** while keeping the RL algorithm and budget fixed.

---

## 4. Direct RL–SBJTS versus RL–Merton result

The comparison evaluates both learned arms on the same frozen SBJTS target holdout.

Define

\[
\Delta_W
=
E[\text{terminal log wealth}\mid\text{train=SBJTS}]
-
E[\text{terminal log wealth}\mid\text{train=Merton}],
\]

and

\[
\Delta_{\mathrm{CVaR}}
=
E[\text{CVaR log loss}\mid\text{train=SBJTS}]
-
E[\text{CVaR log loss}\mid\text{train=Merton}].
\]

Thus \(\Delta_W>0\) and \(\Delta_{\mathrm{CVaR}}<0\) favour SBJTS training.

### 4.1 LONG_ONLY_FULL

| Endpoint | SBJTS mean | Merton mean | SBJTS − Merton | 95% interval |
|---|---:|---:|---:|---:|
| terminal log wealth | 0.0148430 | 0.0126367 | **+0.0022063** | **[+0.0021726, +0.0022423]** |
| CVaR log loss | 0.0838585 | 0.0870395 | **−0.0031810** | **[−0.0033636, −0.0029956]** |

On the log scale, the wealth contrast is approximately **+22.1 bp**, while the CVaR log-loss contrast is approximately **−31.8 bp**. These are horizon-level effects and are not annualised.

### 4.2 LONG_ONLY_CAP50

| Endpoint | SBJTS mean | Merton mean | SBJTS − Merton | 95% interval |
|---|---:|---:|---:|---:|
| terminal log wealth | 0.00752284 | 0.00696874 | **+0.00055409** | **[+0.00054500, +0.00056374]** |
| CVaR log loss | 0.0415466 | 0.0423077 | **−0.00076106** | **[−0.00081033, −0.00071250]** |

The same direction appears under the tighter 50% cap, but the effect is materially compressed. Relative to the FULL stratum, the CAP50 effect is approximately 25.1% as large for wealth and 23.9% as large for CVaR.

This constraint attenuation should be treated as a substantive finding: the economic value of richer market-law training is largest when the policy has enough action freedom to respond to state information.

### 4.3 Secondary outcomes

The FULL stratum also shows:

- VaR log loss: \(-0.0029646\), interval \([-0.0032638,-0.0026690]\);
- max-drawdown q95: \(-0.0005647\), interval \([-0.0007879,-0.0003408]\);
- q01 terminal wealth: \(+0.0029547\), interval \([+0.0024152,+0.0035306]\).

The severe-loss-probability interval crosses zero, so that endpoint should not be used as a headline result.

CAP50 shows the same broad pattern in VaR, drawdown and q01 terminal wealth, again at smaller magnitude.

---

## 5. Earlier Base 4 result: why the Merton comparison is scientifically plausible

Before introducing Merton directly, Base 4 compared SBJTS target training with a corrected no-jump control designed to approximately match canonical one-step mean and variance.

For LONG_ONLY_FULL, Base 4 estimated:

\[
\Delta_W^{\text{SBJTS-control}}
=+3.809735\times10^{-4},
\]

with interval

\[
[+3.6190,+4.0079]\times10^{-4},
\]

and

\[
\Delta_{\mathrm{CVaR}}^{\text{SBJTS-control}}
=-6.137117\times10^{-4},
\]

with interval

\[
[-6.6569,-5.6428]\times10^{-4}.
\]

CAP50 reproduced the direction with smaller effects.

The important mechanism result was the variance decomposition

\[
\operatorname{Var}\left(\sum_t r_t\right)
=
\sum_t\operatorname{Var}(r_t)
+
2\sum_{s<t}\operatorname{Cov}(r_s,r_t).
\]

The diagonal/time-local variance contribution was approximately matched:

\[
\text{diagonal ratio}=0.996409,
\qquad
95\%\ \text{interval }[0.989078,1.004246],
\]

whereas the terminal variance was not:

\[
\text{terminal variance ratio}=1.274346,
\qquad
95\%\ \text{interval }[1.254713,1.292400].
\]

The residual is accounted for by the cross-time covariance/dependence term. The identity was verified on 20/20 validation seeds with maximum numerical error \(1.39\times10^{-17}\).

This Base 4 result supplies the mechanism-level bridge to the direct Merton comparator:

\[
\boxed{
\text{matching local moments}
\not\Rightarrow
\text{matching temporal law}
\not\Rightarrow
\text{equivalent RL training problem}
}
\]

The direct Merton effect is descriptively about 5–6 times larger than the Base 4 corrected-control effect, depending on endpoint and constraint. This ratio is useful only as a magnitude comparison; it is **not** a causal decomposition because the Merton and corrected-control comparators are different counterfactual laws.

---

## 6. Why the result is not just “taking more risk”

A useful paper-level interpretation is that the new comparison is not primarily an average-exposure story.

For FULL, the mean executed action is approximately

\[
0.50068\quad\text{for SBJTS training}
\]

versus

\[
0.49976\quad\text{for Merton training}.
\]

For CAP50, the corresponding values are approximately 0.24991 and 0.24967.

The two learned arms therefore carry nearly the same average exposure, and neither piles probability mass on the hard action boundaries. Yet terminal wealth and tail-risk outcomes differ materially.

This points toward **state-contingent feedback** rather than a simple average-risk-budget explanation. The paper should therefore emphasise that the economic value of SBJTS training appears through *when* the policy changes exposure, not merely through *how much* risky exposure it holds on average.

A direct policy-response analysis is still needed to make this mechanism visible rather than inferred.

---

## 7. Exploratory Merton benchmark and the entropy-time-scaling result

A scientifically important clarification emerged while constructing the direct Merton comparator.

The original continuous-time exploratory Merton objective has the form

\[
J_{\mathrm{cont}}
=
E[\log W_T]
+
\lambda\int_0^T H(\pi_t)\,dt,
\]

whereas the frozen discrete learner uses

\[
J_{\mathrm{disc}}
=
E[\log(W_T/W_0)]
+
m\sum_{t=0}^{N-1}H(\pi_t).
\]

On a grid with step \(\Delta t\), these coincide when

\[
\boxed{m=\lambda\Delta t}.
\]

With \(\Delta t=1/250\):

\[
m=0.01
\quad\Longleftrightarrow\quad
\lambda_{\mathrm{equiv}}=\frac{0.01}{1/250}=2.5.
\]

Conversely, the paper's nominal \(\lambda=0.01\) corresponds to

\[
m=4\times10^{-5}.
\]

Thus equal numerical labels for \(m\) and \(\lambda\) do not represent the same exploration intensity.

The discrete-vs-continuous scaling tests confirm the identity numerically: refining the time grid preserves the optimal executed policy only when the discrete entropy weight is rescaled with \(\Delta t\). This is not a defect in the comparator because both learned arms use exactly the same frozen discrete objective. It does, however, change how the analytic Merton benchmark must be interpreted.

For the manuscript, two analytic Merton conventions should be reported separately:

1. **frozen-learner-equivalent:** \(\lambda=m/\Delta t=2.5\), which is the like-for-like analytic reference for the learner actually used;
2. **paper-nominal:** \(\lambda=0.01\), retained as a link to the original paper's nominal exploration setting.

The analytic benchmark is secondary; it should not replace the learned RL–Merton arm.

---

## 8. The theoretical section that should now be written

The empirical results are strong enough to fix the theory target. The paper should prove the interaction between SBJTS and RL formally rather than describing SBJTS as an external simulator.

### Proposition 1 — wealth coupling

With

\[
g(\pi,r)=\log\left[1+\pi(e^r-1)\right],
\]

we have

\[
\log W_{t+1}=\log W_t+g(\pi_t,r_t).
\]

Hence the market transition law directly determines the reward and next observed state distribution.

For small \(r\),

\[
g(\pi,r)
=
\pi r
+
\frac12\pi(1-\pi)r^2
+O(r^3),
\]

which explains why matching first-two local moments is a natural but incomplete control.

### Proposition 2 — local moment matching does not imply RL equivalence

For two laws \(L_A,L_B\), equality of pooled

\[
E[r_t],\qquad \operatorname{Var}(r_t)
\]

does not imply

\[
J_{L_A}(\theta)=J_{L_B}(\theta)
\]

or

\[
\nabla_\theta J_{L_A}(\theta)=\nabla_\theta J_{L_B}(\theta),
\]

when their conditional/path laws differ. Base 4 provides the empirical covariance-decomposition evidence for precisely this case.

### Proposition 3 — policy gradient under a history-dependent market law

Let \(H_t\) denote the full market history/internal environment state and let the observable learner state be \(s_t=s(H_t,W_t)\). Under a transition law independent of actor parameter \(\theta\), the likelihood-ratio gradient remains

\[
\nabla_\theta J_L(\theta)
=
E_L\left[
\sum_t
\nabla_\theta\log\lambda_\theta(\pi_t\mid s_t)
A_t^L
+
m\sum_t\nabla_\theta H_t
\right],
\]

with the expectation and advantage determined by market law \(L\).

The theorem should be stated on trajectory histories so that the observable four-dimensional policy state need not be falsely claimed to be the complete Markov state of SBJTS.

### Proposition 4 — training-law gradient decomposition

For SBJTS \(S\) and Merton \(M\), write the gradient schematically as

\[
\nabla J_L
=
\sum_t\int
\psi_\theta\lambda_\theta
\,d_L^\theta A_L^\theta,
\]

where \(d_L^\theta\) is the state/history occupancy induced by law \(L\).

Then

\[
d_SA_S-d_MA_M
=
(d_S-d_M)A_S+d_M(A_S-A_M).
\]

This separates two channels:

- **occupancy channel:** SBJTS and GBM visit different histories/states;
- **continuation-value channel:** the same state/action can have different future value under different conditional laws.

This decomposition should be the mathematical centre of the paper's “RL × SBJTS interaction” contribution.

---

## 9. Remaining mechanism evidence needed before final manuscript lock

No new large training run is required for the next stage. The existing frozen policies should be used to produce low-cost mechanism diagnostics.

### 9.1 Conditional-law surface

Show that target SBJTS and its simpler comparators can have similar unconditional moments but different conditional behaviour, e.g.

\[
E[r_t\mid r_{t-1}],
\quad
\operatorname{Var}(r_t\mid r_{t-1}),
\quad
q_{0.05}(r_t\mid r_{t-1}).
\]

This turns the temporal-dependence statement into a visible transition-law result.

### 9.2 Policy response surface

For frozen learned policies, hold \(t\) and wealth fixed and sweep \(r_{t-1}\). Plot

\[
E[\pi_t\mid s_t]
\]

and policy dispersion for RL–SBJTS versus RL–Merton.

This is the most direct figure for showing that the two market laws teach different feedback rules.

### 9.3 Lag-information ablation

Evaluate the frozen SBJTS-trained policy after replacing or shuffling the observed \(r_{t-1}\) input while keeping the same target market paths. If performance degrades, this supplies direct evidence that the learned policy exploits temporal information rather than merely carrying a different average exposure.

These mechanism experiments should be treated as explanatory analyses, not as new headline performance trials.

---

## 10. Contribution statement for the paper

The manuscript can now be framed around four contributions.

### Contribution A — market-law extension

Extend exploratory Merton portfolio RL from a diffusion training environment to a history-dependent SBJTS training law while preserving the constrained stochastic policy architecture.

### Contribution B — theoretical interaction

Show that matching unconditional/local first-two moments does not make two training laws RL-equivalent when their conditional/path dependence differs, and express the resulting policy-gradient difference through occupancy and continuation-value channels.

### Contribution C — computational design

Provide a reproducible constrained actor–critic implementation in which the market law, policy law and learning algorithm are cleanly separated, allowing the training environment to be changed without changing the RL learner.

### Contribution D — empirical evidence

On a frozen SBJTS target holdout, show that SBJTS-trained policies deliver higher terminal log wealth and lower CVaR log loss than both:

1. a corrected no-jump control in Base 4; and
2. an empirically calibrated Merton/GBM training law in the direct comparator.

The Merton comparison is the cleanest headline result because it connects directly back to the original exploratory-Merton paper.

---

## 11. Paper claims that are now supportable

Recommended manuscript wording:

> **In the studied SBJTS target environment, training the same exploratory RL learner under SBJTS rather than an empirically calibrated Merton/GBM law produces higher terminal log wealth and lower tail loss across both long-only constraint strata.**

> **The result is consistent with the hypothesis that temporal and conditional structure omitted by the diffusion training law matters for state-contingent portfolio learning.**

> **Earlier moment-matched-control experiments show that approximately matching one-step first-two moments does not remove the difference in cross-time covariance structure or the resulting training-law effect.**

Claims to avoid:

- “SBJTS universally dominates Merton.”
- “The improvement is a pure jump effect.”
- “The full SBJTS distribution is matched by the control except for jumps.”
- “The current experiment proves external-market superiority.”
- “The four-dimensional learner state is the full Markov state of SBJTS.”
- “The paper's nominal \(m=0.01\) and the discrete learner's \(m=0.01\) represent the same continuous-time exploration intensity.”

---

## 12. Limitations that belong in the scientific paper

The final manuscript should disclose four main limitations without letting them dominate the contribution.

1. **Simulation-based target holdout.** The main comparator is evaluated on frozen SBJTS target environments, not on a large collection of independent realised historical market paths.
2. **Base 2 ancestry.** The frozen SBJTS calibration foundation remains smoke-scale; stronger external-validity language requires a separate research-scale calibration/validation study.
3. **Single exploration setting.** The learned-policy comparison is at frozen discrete \(m=0.01\); exploration heterogeneity is not identified by the current study.
4. **Partial observation.** The policy uses a compact observed state, not the full latent/history state of the SBJTS engine.

Base 4 also carries an unmatched terminal-moment caveat in the corrected-control analysis. That caveat should remain attached to that specific control comparison and should not be mechanically transferred to the distinct empirical-Merton comparison.

---

## 13. Proposed paper structure

### 1. Introduction

Start from exploratory Merton RL and pose the model-misspecification question: what happens when an RL portfolio policy trained in a diffusion world is deployed in a market with SBJTS-type temporal/jump structure?

### 2. Related framework: exploratory Merton control

Present the original continuous-time benchmark, constrained exploratory policy and entropy regularisation, including the time-scaling distinction needed for the discrete implementation.

### 3. SBJTS market law and RL coupling

Define the environment law, observable policy state, wealth recursion and the four theoretical propositions above.

### 4. Learning algorithm

Describe the common actor, truncated-Gaussian policy, critic, soft return, policy-gradient update, constraints and frozen training budget.

### 5. Experimental design

Present two complementary comparisons:

- **Base 4:** SBJTS versus corrected no-jump control with approximate local moment matching;
- **Direct comparator:** RL–SBJTS versus empirical RL–Merton/GBM on the same target holdout.

### 6. Results I — local moments versus temporal law

Report Base 4, especially the diagonal/off-diagonal variance decomposition and constraint attenuation.

### 7. Results II — direct RL–Merton comparator

Make the +0.0022063 wealth and −0.0031810 CVaR FULL effects the headline quantitative result, followed by CAP50 and secondary endpoints.

### 8. Mechanism

Show conditional-law surfaces, policy response surfaces and the lag-information ablation.

### 9. Discussion

Interpret the result as a training-environment/model-misspecification effect; discuss constraints, partial observation, entropy scaling, and limits of simulated target evidence.

### 10. Conclusion

Conclude that richer conditional market dynamics can matter materially to exploratory portfolio RL even when the RL architecture itself is unchanged.

---

## 14. Figures and tables to build

### Main figures

1. **System diagram:** SBJTS/Merton law → returns → wealth → observed state → truncated-Gaussian actor → action → next wealth.
2. **Temporal-law figure:** matched diagonal variance versus divergent cross-time covariance / terminal variance.
3. **Main effect forest plot:** RL–SBJTS minus RL–Merton for wealth and CVaR under FULL and CAP50.
4. **Policy response figure:** expected action versus \(r_{t-1}\) for frozen SBJTS and Merton policies.
5. **Lag ablation figure:** loss of SBJTS-policy performance when temporal state information is removed or shuffled.

### Main tables

1. Environment and learner definitions.
2. Merton empirical calibration and training-design parity.
3. Base 4 target-versus-control results.
4. Direct SBJTS-versus-Merton primary/secondary results.
5. Analytic Merton benchmark under the two entropy conventions.

---

## 15. Current paper-readiness conclusion

The empirical core of the manuscript is now strong enough to be treated as **substantially complete**.

The project no longer needs another large comparator training campaign before drafting the paper. The highest-value remaining work is theoretical and explanatory:

\[
\boxed{
\text{formal RL–SBJTS coupling derivations}
\rightarrow
\text{policy-response / temporal-information mechanism diagnostics}
\rightarrow
\text{manuscript assembly}
}
\]

The direct Merton comparator materially improves the paper because it closes the conceptual loop back to the original exploratory-Merton framework. The central paper message can now be fixed as:

> **A diffusion-trained exploratory RL policy can be systematically misspecified for a market with SBJTS-type conditional dynamics. When the same learner is trained under the richer SBJTS law, it learns a different state-contingent decision rule and, in the tested target environment, achieves higher wealth and lower tail loss.**

The next work should therefore focus on proving and visualising the middle of that causal/scientific chain rather than accumulating more headline performance numbers.

---

## Evidence used for this scientific synthesis

- Frozen Base 4 final results handover, protocol `c9ef65485a49d40356f3bbb02d491c4b73fcc9ebf0a22f02f64ab87e04a590d4`.
- User Colab research outputs from `merton_comparator_v1/evidence/research/`, generated 2026-09-21 on NVIDIA Tesla T4.
- `primary_estimands.json`: 80/80 Merton policies completed; 24,000/24,000 learned-Merton evaluations; 24,000 frozen SBJTS TT rows reused; 1,200 analytic-Merton evaluations.
- `reproduction_check.json`: two-holdout Base 4 reproduction passed bitwise exactly on all 16 predeclared rows.
- `merton_calibration.json`: empirical GBM calibration from the frozen training slice only.
- `entropy_time_scaling_tests.json`: discrete-versus-continuous entropy scaling identity and grid-invariance tests.
