# PMO Manuscript Theory-Consistency Patch Audit v1

**Date:** 2026-09-28  
**Submission:** `ea86d118c3c484a0b8fa5a1c48e2f27bebcf0f21`  
**Branch audited:** `claude/epic-babbage-andjdj`  
**Base before merge:** `72820e0fb346e3cd8bd75aa3ef9e5b9e19aea455`  
**Verdict:** `ACCEPTED / MERGED_TO_MAIN`

## 1. Scope and lineage

The branch was exactly one commit ahead of `main` and zero commits behind. The diff contained exactly two files:

- `rl_sbjts/manuscript/RL_SBJTS_MANUSCRIPT_DRAFT_v1.tex` — modified, 57 additions / 8 deletions;
- `rl_sbjts/reports/pmo/RL_SBJTS_THEORY_SUPERSESSION_NOTE_v1.md` — new, 41 lines.

No research evidence, frozen notebook, estimand, experiment, accepted theory report, or current-state file was modified by Claude. The submission is editorial/theory-consistency work only.

## 2. T3 audit — accepted

The manuscript now states A1--A4, retains the fact that the four-feature learner observation is not assumed to be a complete Markov state, and distinguishes the policy-parameter score from the full actor-weight score that chains through the state vector.

The full two-term gradient is now carried explicitly:

\[
\nabla_\theta J_L
=
E\left[R^{\rm soft}_\theta(\tau)\sum_t\psi_\theta(A_t,S_t)\right]
+
mE\left[\sum_t\partial_\theta H(\lambda_\theta(\cdot\mid S_t))\right].
\]

The direct entropy derivative is kept separate. The manuscript also states the accepted mixed sufficient condition

\[
\sup_{\theta\in U}E\left[(1+\max_{t\le N}\|S_t\|)(1+|R^{\rm soft}_\theta|)\right]<\infty,
\]

as an assumption, not a verified property of the frozen SBJTS law. The withdrawn reduction to terminal-log-wealth first-moment integrability does not reappear.

## 3. T4 audit — accepted

The manuscript now introduces a common dominating measure before the symmetric occupancy/continuation-value split and correctly notes that the two occupancy laws need not share support.

The symmetric midpoint identity is retained as an attribution convention rather than a causal decomposition. The full law-gap discussion now carries three pieces:

1. symmetric occupancy contribution;
2. symmetric continuation-value contribution;
3. direct entropy-derivative occupancy-difference contribution.

The third term is not dropped merely because it vanishes on the enumerable verification fixture.

## 4. T5 audit — accepted

The covariance identity is immediately followed by the required local caveat: the result establishes availability of a lag-dependent conditional-information channel, not attribution of a particular share of the wealth/CVaR gap to lagged return alone. Occupancy, continuation-value, wealth-state, and higher-order channels remain unseparated.

For manuscript interpretation, the relevant statement remains the conditional-mean covariance channel; the paper should not broaden this into a claim that every possible lag-related policy effect disappears under iid Merton.

## 5. Supersession note — accepted

`RL_SBJTS_THEORY_SUPERSESSION_NOTE_v1.md` correctly preserves the accepted theory report unchanged while recording that:

- the historical P3 first-moment reduction is superseded by P6;
- A4 / A4-mixed is authoritative;
- the conditional-law diagnostic is no longer pending and has been accepted;
- lag-ablation retraining remains unauthorized;
- the raw actor lag coefficient (about `-1.56`) and executed-policy lag-response slope (about `-0.674` in LONG_ONLY_FULL) are distinct quantities and must not be interchanged.

## 6. Compilation and editorial status

Claude reports a clean two-pass `pdflatex` build with no errors or overfull boxes, and no build artifacts were committed. PMO did not rerun research or alter any scientific artifact during this audit.

## 7. PMO decision

The patch is scientifically consistent with the accepted T1--T5 package and closes the identified manuscript-theory omissions. Commit `ea86d118...` was fast-forwarded to `main` without force.

**No additional model development or research-scale experiment is opened.**

Next work is final manuscript claim/reference/literature audit, journal-template adaptation, language/figure polish, and advisor/reviewer response preparation.
