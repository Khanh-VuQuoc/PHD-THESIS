# C-RLSBJTS-THEORY-COUPLING-01 — Formal theory coupling and theorem-to-code verification

**Status:** `READY_FOR_PMO_THEORY`  
**Owner:** Claude — Technical Research Verifier / Implementation Lead  
**PMO:** GPT  
**Execution policy:** derivation + code mapping + static/unit/smoke only; **no research-scale training or evaluation**.

## 1. Scientific objective

Convert the completed empirical RL–SBJTS versus RL–Merton result into a rigorous theory section explaining how the training market law enters the reinforcement-learning problem and why a history-dependent SBJTS law can produce a different learned feedback policy even when local unconditional moments are similar.

The authoritative starting documents are:

1. `../00_CURRENT_STATE.md`
2. `../reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md`
3. `../reports/research/RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md`
4. `../reports/research/RL_SBJTS_THEORY_COUPLING_BLUEPRINT_v1.md`
5. frozen Base 3 learner and Base 4 scientific implementation sources referenced by `04_CANONICAL_SOURCE_MAP.md`.

Do not reopen Base 4 or retrain any policy.

## 2. Required theorem/proposition package

### T1 — exact wealth coupling

Formalize

\[
W_{t+1}=W_t[(1-A_t)R_t^f+A_t e^{r_t}],
\]

and for the primary `R_t^f=1` convention,

\[
X_{t+1}-X_t=\log\{1+A_t(e^{r_t}-1)\}.
\]

Derive the small-return expansion through at least third order and state exactly which return moments/path features can enter expected growth beyond the first two moments.

### T2 — local moment matching does not imply RL equivalence

Prove a narrow non-equivalence proposition: equality of unconditional one-step mean and variance does **not in general** imply equality of soft value functions, policy gradients, or learned policies when higher moments or conditional/path laws differ.

Provide either a constructive counterexample or a formal functional argument. Do **not** claim that every moment-matched pair must generate different policies.

### T3 — trajectory policy gradient under history dependence / partial observation

Let `H_t` be the full simulator history state and

\[
S_t=(1,t/N,\log(W_t/W_0),r_{t-1})
\]

be the learner observation. Prove the likelihood-ratio gradient for an observation-based policy without assuming `S_t` is a complete Markov state.

The proof must state assumptions under which

\[
\nabla_\theta \log p_{\theta,L}(\tau)
=\sum_t \nabla_\theta\log\lambda_\theta(A_t\mid S_t)
\]

holds, especially that the environment transition kernel has no direct dependence on actor parameter `theta`.

Treat the frozen discrete entropy objective carefully:

\[
J_L(\theta)=E[X_N-X_0+m\sum_t H(\lambda_\theta(\cdot\mid S_t))].
\]

Distinguish the trajectory-score contribution from the direct entropy derivative. If an advantage form is used, define the soft return/advantage precisely.

### T4 — SBJTS-versus-Merton interaction decomposition

Define a full-history occupancy measure `d^theta_{L,t}` and a soft action advantage. Derive the decomposition

\[
d_SA_S-d_MA_M=(d_S-d_M)A_S+d_M(A_S-A_M),
\]

and interpret the two terms as:

1. **occupancy channel**;
2. **continuation-value channel**.

If the entropy derivative is not folded into the soft advantage, state the additional entropy-occupancy term explicitly.

### T5 — structural role of lagged return

Show mathematically why under iid GBM the next innovation does not become predictable from `r_{t-1}`, whereas under a history-dependent SBJTS transition law `E[r_t | H_t]` can depend on path information. Connect this to

\[
E[\pi_t r_t]=E[\pi_\theta(S_t)E(r_t\mid S_t)].
\]

Keep the conclusion structural: the current empirical policy-response surface is consistent with this mechanism, but it does not prove lagged return is the sole causal channel.

## 3. Entropy-time-scaling discipline

Carry forward the already verified distinction:

\[
J_{disc}=E[X_N-X_0]+m\sum_t H_t,
\qquad
J_{cont}=E[X_T]+\lambda\int H_t dt,
\]

with `m = lambda * dt`. At `dt=1/250`, frozen `m=0.01` corresponds to `lambda=2.5`.

This does not alter the direct learned-arm comparator because both arms use the same frozen discrete objective. It must remain explicit in all analytic-Merton references.

## 4. Theorem-to-code verification table

Produce a table mapping each mathematical object to the exact implementation function/cell/source and a cheap verification test:

- state map;
- wealth recursion;
- truncated-Gaussian density/normalization;
- raw-to-policy transform;
- entropy;
- soft return-to-go;
- critic target/value fit;
- actor score / gradient sign;
- actor-parameter independence of the market kernel;
- seed namespaces / no hidden wall-clock seeding.

Use source inspection and tiny unit/smoke tests only.

## 5. Required cheap gate-mutation controls

Without running research training, add or execute fixture-level mutation checks demonstrating that the load-bearing gates can fail:

- corrupt U0 source/hash identity -> gate fails;
- corrupt U1 reference row/attempt id -> reproduction gate fails;
- corrupt U2 calibration tolerance/known synthetic moment -> calibration gate fails;
- corrupt U3 learner/plumbing fixture -> positive-control gate fails.

These are specificity/unit tests only. They must not create paper-effect estimates.

## 6. Claim discipline

Do not claim:

- truncated Gaussian is globally optimal under SBJTS;
- the four-feature observation is a complete Markov state;
- the comparator isolates a pure jump effect;
- lagged return alone causes the performance gain;
- universal superiority of RL–SBJTS.

The accepted empirical claim is domain-scoped: under the tested frozen SBJTS deployment law, the SBJTS-trained learner outperforms the matched empirical-GBM-trained learner on terminal log wealth and CVaR log loss in both frozen constraint strata.

## 7. Allowed outputs

Claude may create/update only:

- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- optionally `evidence/theory_coupling_v1/unit_checks.json`
- optionally `evidence/theory_coupling_v1/theorem_code_map.csv`
- this ticket's `Status` / `Progress` section.

Do not modify frozen evidence, comparator research outputs, PMO state, claim ledger, decision log, or PMO skill.

## 8. Completion response

Return:

```text
STATUS: READY_FOR_PMO_THEORY or BLOCKED
FILES_CHANGED:
PROPOSITIONS_PROVED:
ASSUMPTIONS:
THEOREM_TO_CODE_MAP:
UNIT/MUTATION_TESTS:
UNRESOLVED_THEORY_ISSUES:
CLAIM_DISCIPLINE:
COMMIT:
```

Then mark the ticket `READY_FOR_PMO_THEORY` and stop. No full training/evaluation is authorized.

## 9. PMO audit of first theory submission

**Submission audited:** commit `64cd35b0d885a5306733a5c7ea4ea75a8ba0fd18`  
**PMO verdict:** `TARGETED_PATCH`.

The first submission is accepted in substance: T1–T5 core structure, the theorem-to-code map, frozen-source identity, entropy scaling, and unit/mutation evidence are strong. No research-scale rerun is requested. The patch is limited to mathematical precision and manuscript-safe decomposition.

### Required patch P1 — localize the T1 moment series

Keep the exact identity

\[
g(a,r)=\log\{1+a(e^r-1)\}
\]

global. But the Taylor expansion and any representation as an infinite sum of conditional moments must be labelled **local/asymptotic around `r=0`**, unless explicit convergence and expectation/series interchange conditions are stated. Do not write an unconditional exact equality `E[g]=sum_k ...` for jump steps without those conditions. Preserve the existing caveat that the exact coupling, not the truncated series, governs jumps.

### Required patch P2 — correct the market-entry wording

Replace any wording equivalent to “the market enters the learning problem only through this scalar map.” The scalar map is the exact **one-step wealth coupling**, but the market law also changes the distribution of future history/observations, occupancy measures and continuation values. The paper's central mechanism requires both roles.

### Required patch P3 — strengthen T3 regularity assumptions

Do not justify differentiation-under-expectation by claiming that SBJTS returns have bounded support. State an explicit sufficient domination/integrability assumption, for example finite integrability of the score-weighted soft return and entropy derivative in a neighbourhood of `theta`, together with the smooth bounded policy transform/action interval. If a stronger moment condition is used, state it as an assumption rather than as a verified property of the stochastic law unless source evidence proves it.

### Required patch P4 — correct T3.4 finite-difference language

A central finite difference at nonzero step size is a numerical approximation with truncation error (typically `O(h^2)` under the required smoothness); it is not literally an unbiased pathwise estimator. Rephrase T3.4 as an independent numerical agreement check between the likelihood-ratio gradient and a common-random-number pathwise/finite-difference approximation, with both Monte Carlo uncertainty and finite-difference error acknowledged. Do not use the finite-difference check as the proof of T3; the proof is analytic.

### Required patch P5 — make T4 manuscript decomposition symmetric/reference-explicit

The first submission correctly discovered that the two-channel split is reference dependent. For the main manuscript, use the symmetric midpoint identity

\[
d_SA_S-d_MA_M
=\tfrac12(d_S-d_M)(A_S+A_M)
+\tfrac12(d_S+d_M)(A_S-A_M),
\]

under a common dominating measure, and label the two terms as a **symmetric occupancy contribution** and a **symmetric continuation-value contribution**. State clearly that even this is an attribution convention, not a causal identification. Keep the S-reference and M-reference decompositions as supporting/appendix identities demonstrating non-uniqueness. If the direct entropy derivative remains outside the soft advantage, carry its occupancy-difference term separately. Add the symmetric split to the exactly enumerable fixture and verify that it sums to the same total gap.

### Patch acceptance

- No new training or research-scale evaluation.
- Re-run only the cheap theory/unit fixture if needed.
- Update the report and machine-readable evidence/map where the corrected statements affect them.
- Preserve all existing caveats on partial observation, critic finite-sample bias, non-pure-jump interpretation and entropy scaling.
- Sync current `main` before patching; do not overwrite PMO state/decision files.

After these five items are addressed, return `READY_FOR_PMO_THEORY` again and stop.

## 10. Progress

### 2026-09-22 — Claude — first submission — `READY_FOR_PMO_THEORY`

Commit `64cd35b0d885a5306733a5c7ea4ea75a8ba0fd18`. T1–T5 proved and verified against
the frozen sources; 18 check groups, 16 theorem-to-code rows, 20/20 gate-mutation
controls. Audited by PMO as `TARGETED_PATCH` (§9, DEC-RL-005).

### 2026-09-22 — Claude — patch submission — `READY_FOR_PMO_THEORY`

Targeted patch of the existing submission only. No new training or research-scale
evaluation; the cheap theory/unit fixture was re-run in full (115.9 s on CPU) and all
18 check groups plus all 18 theorem-to-code rows pass. Frozen-source identity
re-confirmed (Base 3 code-cell concat `db500333b57ae902…`, training slice
`09811db465da1443…`, 17/17 native AST components, 0 mismatches). PMO state, decision
log, claim ledger and frozen evidence untouched; `main` synced before patching.

**P1 — localize the T1 moment series.** The exact coupling stays global. The
moment-series statement is now the finite-order form with an explicit remainder,
labelled local/asymptotic around `r = 0`. A new §T1.3 supplies explicit convergence
and interchange conditions instead of a hand-wave: the singularities of
`log(1+a(e^r-1))` sit at `r = log(1/a-1) ± iπ`, so the radius of convergence is
`sqrt(log^2(1/a-1) + π^2) ≥ π`, minimised at `a = 1/2` where it equals exactly `π`.
Verified in closed form (`1 + ½(e^{iπ}-1) = 0` exactly; modulus minimised over `a` at
3.14159265358979 with argmin 0.5000) rather than from coefficient asymptotics; the
coefficient root test is demoted to a slowly-converging diagnostic (corrected estimate
3.1014, relative error 1.3%). Recorded as `t1_series_validity` in the evidence file and
as a new theorem-to-code row. The frozen training slice sits at 4.96% of the radius,
but the condition is explicitly **not** verified for the frozen SBJTS jump law.

**P2 — market-entry wording.** The sentence "the market enters the learning problem
only through this scalar map" is removed. §T1 now states the two roles: `g(A_t,r_t)` is
the exact one-step wealth coupling, and `Q_L` additionally determines future
histories/observations, the occupancy measures and hence continuation values, with a
forward reference to T4 showing these are separate channels.

**P3 — T3 regularity.** The bounded-support justification is **withdrawn** and labelled
as such in a new (A4′). (A3) is restated as a structural property of the frozen policy
class (truncated Gaussian, `scale_floor > 0`, smooth bounded transform). (A4) is now an
explicit domination condition: an integrable `Φ(τ)` dominating the score-weighted soft
return plus the entropy derivative on a `θ`-neighbourhood, reduced under (A3) to
first-moment integrability of terminal log wealth. It is stated as an assumption on the
training law, not as a verified property of the stochastic law.

**P4 — T3.4 finite-difference language.** Reframed as an independent numerical
agreement check between the likelihood-ratio gradient and a common-random-number
pathwise central difference, explicitly **not** the proof (the proof is analytic). The
"unbiased pathwise estimator" wording is gone. The `O(h^2)` truncation error is now
named and measured: halving `h` from 1e-4 moves the estimate by at most 6.52e-09
against a smallest paired standard error of 5.99e-06, i.e. about 0.11% of the Monte
Carlo noise. Both error sources are reported side by side.

**P5 — symmetric T4 decomposition.** The symmetric midpoint identity
`½(d_S-d_M)(A_S+A_M) + ½(d_S+d_M)(A_S-A_M)` is adopted as the manuscript
decomposition and added to the exactly enumerable fixture. It sums to the same total
gap (−5.830329e-4) with residual exactly 0.0, and equals the arithmetic mean of the two
reference splits to 2.7e-20. Symmetric occupancy contribution −7.283662e-5, symmetric
continuation-value contribution −5.101963e-4. The S- and M-reference splits are retained
as supporting/appendix identities documenting non-uniqueness (occupancy channel differs
by 1.457e-4 between them). The direct entropy derivative remains outside the soft
advantage and its occupancy-difference term is carried separately. The report states
explicitly that even the symmetric split is an attribution convention, not a causal
identification.

One substantive by-product of P5 worth PMO's attention: the fixture's two occupancy
measures do **not** share a support — under the mirror chain half the length-2 return
prefixes carry zero mass, so `d_S << d_M` but not conversely. The symmetric identity
therefore needs its dominating measure named, and the report names it (counting measure
on the 6-point union). One-sided absolute continuity is the generic situation whenever
the training law constrains reachable histories, so the manuscript should state the
dominating measure rather than assume a shared support.

Preserved unchanged, as required: the partial-observation treatment (`S_t` is nowhere
assumed Markov), the critic finite-sample-bias caveat (0.54 SE), the non-pure-jump
interpretation, the entropy time-scaling discipline (`m = λ·dt`, frozen `m=0.01` ↔
`λ=2.5`), and the T5 non-claim. The `SCOPE CHANGE REQUEST — PMO DECISION REQUIRED` for
the conditional-law / lag-ablation diagnostic also stands: still specified, still not
executed.

### 2026-09-22 — Claude — P6 patch submission — `READY_FOR_PMO_THEORY`

P6 only, per `reports/pmo/PMO_THEORY_COUPLING_PATCH_AUDIT_v2.md`. **T1–T5 substance is
unchanged**; the diff is confined to T3 regularity, the two score rows of the
theorem-to-code map, and one housekeeping fix noted below. No training, holdout
evaluation, Colab run or new empirical estimand. Cheap unit/static fixture re-run in
full: 117.8 s on CPU, 20 gated check groups and 19 theorem-to-code rows all pass. `main`
synced first; PMO state, decision log, claim ledger and frozen evidence untouched.

**The audit is right, and the previous reduction was wrong.** `grad_theta log lambda` is
not dominated by the bounded policy transform, because the frozen actor is linear in the
state: `raw_k = S_t . w[k]`, so the chain rule gives

    grad_{w[k]} log lambda = [ J_transform(raw)^T grad_phi log lambda ]_k * S_t,

and `S_t` carries `log(W_t/W_0)`, which nothing bounds.

New §T3.0 in the report distinguishes the two scores and establishes the point rather
than asserting it:

- **Static source evidence.** The frozen `actor_gradient` literally contracts against the
  state matrix — `grad = np.einsum("ptk,ptf->kf", coeff, S)` with `S = roll["states"]` —
  `LinearActor.latent` returns `S @ self.w[0], S @ self.w[1]`, and `state_features`
  returns `np.stack([ones, tt, lw, pr], axis=-1)` with `lw` a free float argument carrying
  no clip, bound or truncation. All four checks True.
- **Chain rule verified numerically.** Against central differences in the actor weights,
  worst relative error 3.0e-09 at h = 1e-6. Relative rather than absolute because the
  quantity being checked itself scales with the state norm.
- **Witness of non-uniform-boundedness.** At a parameter point whose raw outputs carry no
  state feedback, `score_phi` is exactly constant (norm 8.511 across the whole sweep)
  while `||grad_w log lambda||` runs 45.30 -> 967.01, with the ratio to `||S_t||` constant
  to 7.1e-15 and the growth factor matching the state-norm growth factor to the digit
  (21.346x versus 21.346x). Since the log-wealth coordinate is unbounded,
  `sup_s ||grad_theta log lambda|| = infinity`.
- **Contrast regime, recorded deliberately.** With a non-zero wealth coefficient the raw
  output is driven into `tanh` saturation, `J_transform -> 0` exponentially, and the same
  norm *decays* (0.161x over the identical sweep). So the transform yields neither a
  uniform bound nor a uniform growth rate, and the behaviour is direction dependent. The
  manuscript should not overclaim in either direction.

**Assumption changes.** The reduction of (A4) to `E|X_N-X_0| < infinity` is **withdrawn**
and named as withdrawn in (A4'), alongside the previously withdrawn bounded-support
rationale. (A4) stays a general domination assumption, and a new (A4-mixed) gives the
explicit mixed state/soft-return moment condition

    sup_{theta in U} E[ (1 + max_{t<=N} ||S_t||) (1 + |R_soft_theta(tau)|) ] < infinity,

with the reason the mixing is necessary: the chain rule multiplies the soft return by the
state norm, so a condition on either factor alone does not dominate the product. Given
(A3) and the compact action interval the per-step factors `||J_transform||` and
`||psi_phi||` are bounded on `U`, so this condition dominates both the score-weighted soft
return and the direct entropy derivative term by term, the finite horizon absorbing the
sum over `t`. It is assumed on the training law and the theorem is presented conditionally
on it, as the audit permits.

**What still transfers.** The zero-mean lemma is unaffected and this is now stated
explicitly: `J_transform` and `S_t` are both `S_t`-measurable, so
`E[grad_theta log lambda | S_t] = [J^T E(psi_phi | S_t)] S_t^T = 0` whenever
`E[psi_phi | S_t] = 0`. The existing T3.1 quadrature check on `psi_phi` therefore
establishes the lemma for the full actor score, and T3.1/T3.2 are relabelled `psi_phi` to
make the scope exact.

**Theorem-to-code map.** The single conflated score row is split into two: a
POLICY-PARAMETER score row (`score_phi`, bounded on the frozen phi box) and an
ACTOR-WEIGHT score row (`grad_theta log lambda = [J_transform^T psi_phi] (x) S_t`, chains
through the state features, not uniformly bounded), the latter carrying the new `t3_6`
verification. Map grows 18 -> 19 rows.

**Housekeeping fix, disclosed.** While wiring `t3_6` in I found that the pass aggregation
ran over a hardcoded list of check names, so `t1_series_validity` (added in P1) and
`t3_6` were written into the evidence file without being covered by `all_pass`. Both
passed on their own, so nothing was misreported, but a gate that silently omits checks is
not a gate. The aggregation now derives its key set from the blocks actually computed and
raises if any of them carries no verdict field instead of defaulting it to pass;
`blocks_recorded_but_not_gated` records the one deliberate exclusion
(`t1_moment_structure`, a record of the expansion polynomials rather than a test). Gated
groups 18 -> 20.

Preserved unchanged: T1 local expansion and its convergence conditions, T2 both
non-equivalence constructions, T4 symmetric midpoint decomposition and the S/M supporting
identities, T5 structural result and non-claim, the partial-observation treatment, the
critic finite-sample-bias caveat, the entropy time-scaling discipline, and the standing
`SCOPE CHANGE REQUEST — PMO DECISION REQUIRED` for the conditional-law / lag-ablation
diagnostic.
