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

## 9. Progress

### 2026-09-22 — Claude — `READY_FOR_PMO_THEORY`

Derivation, theorem-to-code verification and unit/mutation tests complete. No
research-scale training or evaluation was run; no estimand was recomputed; no
claim was created or modified. Execution class `SMOKE_EVIDENCE`; whole package
runs in 74.8 s on CPU.

Delivered against the allowlist in section 7:

- `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md`
- `evidence/theory_coupling_v1/unit_checks.json`
- `evidence/theory_coupling_v1/theorem_code_map.csv`

T1–T5 of the blueprint are proved and verified against the frozen sources
(Base 3 code-cell concat `db500333b57ae902…` and training slice
`09811db465da1443…` both match their pinned digests; 17/17 native AST engine
components, 0 mismatches). All 18 check groups pass, 16 theorem-to-code rows
pass, and 20/20 gate-mutation controls behave as predeclared, 14 of them
negative controls that must fail.

Five items are referred to PMO rather than resolved here, all recorded in
section "Unresolved theory issues for PMO" of the report:

1. The T4 channel decomposition is **not split-invariant** — the occupancy
   channel is −1.457e-4 with the soft advantage referenced at S and exactly
   0.0 referenced at M, a disagreement of about a quarter of the total gap
   (−5.830e-4). Only the total is convention free, so the manuscript must
   declare the reference law. Presentation decision with mathematical content.
2. **`SCOPE CHANGE REQUEST — PMO DECISION REQUIRED`** — the conditional-law
   and lag-ablation diagnostic that would close the T5 attribution is
   specified with a precise estimand but deliberately **not executed**, since
   both parts exceed unit scale and `00_CURRENT_STATE.md` reserves that
   decision for PMO.
3. The fitted critic is a variance-reduction device and is not part of the
   gradient theorem; its measured deviation from the provably unbiased
   unbaselined estimator is 0.54 standard errors.
4. T2b's optimal lag coefficient under the dependent law sits at the boundary
   of the searched grid, so the rigorous content is the exact-zero-versus-
   nonzero derivative contrast at zero, not a magnitude.
5. T1's expansion is a local r→0 statement with a verified O(r⁴) remainder and
   is not the right tool on jump steps; the exact coupling needs no expansion.

The U1 reproduction fixture used by the mutation controls is the SMOKE-only
mechanism subset, not the predeclared two-holdout gate, which cannot pass in
this sandbox (only the first 1 MiB of the 31 MB frozen ledger is retrievable,
so holdout stream 1 has no reference rows). The gate of record remains the
user's Colab T4 run, which returned `BASE4_TARGET_REPRODUCTION_PASS_EXACT` on
all 16 rows.
