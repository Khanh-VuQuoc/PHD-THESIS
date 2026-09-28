# RL–SBJTS reviewer-attack simulation v1

**Date:** 2026-09-28  
**Manuscript:** `manuscript/RL_SBJTS_MANUSCRIPT_DRAFT_v1.tex` at `main` = `6ddb4a5`  
**Execution class:** read-only editorial audit. **No experiment is authorized or requested by this document.**

For every objection, the order of defence is: existing theory → accepted evidence → wording clarification → limitation statement. An objection is marked "new experiment" only where none of these can answer it. Where a *cheap descriptive statistic* on existing frozen inputs would help, it is marked **PMO decision**, not authorized.

Summary: 12 objections — 3 CRITICAL, 7 MAJOR, 2 MINOR. None requires a new experiment for the paper's *current scoped claims*. Two (R5 and R11) could only be *fully* removed by new work, which is not authorized; they are answered by limitation statements.

---

### R1 — "The SBJTS arm is trained on the deployment law itself. Of course in-distribution training beats a misspecified simulator; the result is close to tautological."

- **Severity:** CRITICAL (novelty).
- **Already answered?** Partly. The Introduction frames the study as a misspecification question (l.27–29). Nowhere does it say explicitly that the SBJTS arm trains on the same law it is deployed on (with disjoint seeds).
- **Where:** Intro l.29; Design l.53.
- **Minimal clarification:**
  - State it plainly in Design.
  - Reframe the contribution as *quantifying* the cost of the standard data-calibrated diffusion training law, and *showing how* the learned rule differs, rather than showing that it differs at all.
  - Add that the SBJTS arm is an oracle-law benchmark: it gives an upper reference for the value of training-law fidelity, conditional on SBJTS.
  - Point to the non-trivial parts: the size of the gap at nearly equal mean exposure, the constraint attenuation, and the aligned feedback mechanism.
- **New experiment?** No.

### R2 — "The Merton arm is not moment-matched to the deployment law. Its variance is ~50% lower than SBJTS's unconditional variance and its mean differs, so the gap may simply be a variance-level miscalibration, not path dependence."

- **Severity:** CRITICAL (interpretation).
- **Already answered?** No. The Intro (l.27) and Conclusion (l.179) currently *suggest* moment matching.
  - The values are `PMO_CONDLAW_RESULT_AUDIT_v1.md`: SBJTS variance 0.000262257, Merton 0.000172661; SBJTS mean ≈0.000373, Merton 0.000277.
  - Each is a law-specific statistic of the respective simulator.
- **Where:** —
- **Minimal clarification:**
  - (a) Remove "even when local low-order return moments are matched" from the Conclusion, or support it with Base 4.
  - (b) State in Design that the GBM is calibrated to the historical slice, which is the standard practitioner calibration, and not to the simulator's moments.
  - (c) Point to accepted Base 4 evidence: an affine no-jump control approximately matching canonical one-step mean and variance still differed in path law (diagonal variance ratio 0.996 vs terminal ratio 1.274) and in outcomes. Base 4 numbers come from `RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md` §5 and must be confirmed against the Base 4 handover before quoting — **PMO decision**.
  - (d) Cite T2 for the general statement.
  - (e) List "Merton arm not moment-matched to deployment law" as a limitation.
- **New experiment?** No. A GBM moment-matched to the SBJTS simulator would be a new training run. It is **not needed** once the wording is corrected, and not authorized.

### R3 — "SBJTS is never defined. The simulator's structure, parameters and calibration are not in the paper; nothing is reproducible."

- **Severity:** CRITICAL (reviewability).
- **Already answered?** No. The acronym is never expanded; l.29 and l.47 describe it in one sentence each.
- **Where:** —
- **Minimal clarification:**
  - Add a model section or appendix taken from the existing frozen technical record (`RL_SBJTS_TECHNICAL_IMPLEMENTATION_RECORD_FINAL.md`, referenced in the canonical source map).
  - Cover the state, bridge drift, kernel-weight path functional, and jump intensity and classes (theory report §T5 lists the load-bearing structure).
  - Cite the SBJTS source work.
  - Add a data/code availability statement pointing to the frozen hashes.
- **New experiment?** No. This is documentation only.

### R4 — "Mean exposure is ≈0.500 on [0,1] and ≈0.250 on [0,0.5], the interval midpoints, for *both* arms. The entropy weight (m=0.01, i.e. continuous-time temperature 2.5) looks strong enough that the policies are near maximum-entropy. 'Not explained by exposure' may just mean both arms are pinned to the midpoint."

- **Severity:** MAJOR.
- **Already answered?**
  - Partly: l.44 gives m=λΔt, and the Discussion (l.176) lists one exploration level as a limitation.
  - The temperature equivalent of 2.5 is not stated.
  - The midpoint coincidence is not discussed.
- **Where:** l.44, l.176.
- **Minimal clarification:**
  - State λ_equiv=2.5.
  - Note that both arms' mean actions sit near the interval centre, consistent with strong entropy regularization at the frozen m.
  - Describe the mechanism as state-contingent feedback around that centre: 0.543→0.462 across ±0.06 lag.
  - Soften AB7 ("not accompanied by a material difference in average exposure").
  - Keep the single-exploration-level limitation.
- **New experiment?** No, for the scoped claim. An exploration-level sweep would be new work and is not authorized; this is a limitation.

### R5 — "Deployment is a simulator. There is no evaluation on historical returns, and the simulator's calibration ancestry is described internally as smoke-scale. External validity is nil."

- **Severity:** MAJOR.
- **Already answered?**
  - Partly: l.31 says SBJTS is not claimed to be the true DGP, and l.176 says "the deployment environment is simulated".
  - The smoke-scale ancestry is not disclosed.
- **Where:** l.31, l.176.
- **Minimal clarification:**
  - Add an explicit limitation: the SBJTS calibration derives from a limited-scale calibration study, and no historical-market validity is claimed.
  - Keep all performance statements conditioned on "the tested frozen SBJTS deployment law".
- **New experiment?** Fully removing the objection would require a historical out-of-sample study. That is a new scientific question, **not authorized**. For the current claim, a limitation statement is sufficient.

### R6 — "A lag-1 autocorrelation of −0.125 in daily index-like returns is far stronger than what is typically observed. The SBJTS policy may be exploiting a simulator artifact."

- **Severity:** MAJOR.
- **Already answered?** No.
- **Where:** l.169 reports the number without context.
- **Minimal clarification:**
  - Present the lag structure explicitly as a property of the frozen simulator.
  - Repeat that no claim is made about real-market predictability.
  - Tie this to R5.
- **New experiment?** No. The lag-1 autocorrelation of the frozen *historical training slice* would be a cheap descriptive statistic on an existing frozen input. It is not an experiment and needs no training, but it is **not run** and is left as a **PMO decision**. If PMO declines, the limitation wording is sufficient.

### R7 — "The mechanism is correlational. Without a lag-ablation, you cannot claim the policy's lag feedback produces the gain."

- **Severity:** MAJOR.
- **Already answered?** Yes, in substance:
  - l.31: no claim that the lagged-return channel uniquely causes the gap;
  - l.142: T5 availability caveat;
  - l.176: no causal share.
- **Where:** l.31, l.142, l.176.
- **Minimal clarification:**
  - Label the mechanism section "descriptive" in its first sentence.
  - Add that a lag-ablation contrast was deliberately not run and that the mechanism evidence is directional alignment only.
- **New experiment?** Only for causal attribution, which is not claimed. Lag-ablation retraining remains **NOT AUTHORIZED**.

### R8 — "T3 is the textbook likelihood-ratio/REINFORCE identity, and 'no Markov assumption' is standard for POMDP policy gradients (GPOMDP). T4 is an algebraic identity. Where is the theoretical novelty?"

- **Severity:** MAJOR (novelty).
- **Already answered?** No. Theory is presented without citations.
- **Where:** l.74–142.
- **Minimal clarification:**
  - Cite Williams (1992) and Baxter–Bartlett (2001).
  - Claim novelty only for:
    - (i) the constructive non-equivalence under matched one-step moments or marginals (T2);
    - (ii) the specialization to the constrained truncated-Gaussian learner, with the actor-weight versus policy-parameter score distinction and the mixed domination condition;
    - (iii) the use of a symmetric identity with an explicit entropy-occupancy term to organize the *training-law* gradient gap.
  - Call T3/T4 "framework results" rather than new theorems.
- **New experiment?** No.

### R9 — "The T4 decomposition is never estimated on the actual problem. It is decorative."

- **Severity:** MAJOR.
- **Already answered?** Partly. l.134 says it is an attribution convention. The manuscript does not say it was verified only on an enumerable fixture and not estimated on SBJTS vs Merton.
- **Where:** l.117–134.
- **Minimal clarification:** Add one sentence saying the identity is used conceptually to name the channels through which the training law can act, that it was verified on an exactly enumerable model, and that the channels are not estimated for the frozen experiment.
- **New experiment?** No.

### R10 — "Inference is unclear. What is a 'crossed-cluster' bootstrap? Why are the CIs so narrow? Are the arms paired? Is this a hypothesis test?"

- **Severity:** MAJOR.
- **Already answered?** No. Only "crossed-cluster intervals" and "policy-level sensitivity" are named.
- **Where:** l.23, l.166.
- **Minimal clarification:** In Design, state:
  - clusters are training replication × holdout block;
  - 20 streams × 15 seeds = 300 blocks per policy, 600 paths per evaluation;
  - common random numbers pair the arms on identical target paths;
  - the policy-level analysis collapses the 300 blocks and bootstraps only the 40 paired replications;
  - the analysis is estimation-first, with no prespecified smallest effect size of interest, so the intervals are descriptive precision statements, not a confirmatory test.
  - Do **not** quote the exploratory sign-flip p≈1e-5 (`MECHANISM_AND_ROBUSTNESS_v1` §5) as a test.
- **New experiment?** No.

### R11 — "Results are for one linear actor, a four-feature state, one truncated-Gaussian policy class and two constraints. Nothing generalizes."

- **Severity:** MINOR (for a scoped paper).
- **Already answered?** Partly: l.31 (no global optimality) and l.176 (partial observation).
- **Where:** l.31, l.176.
- **Minimal clarification:** Add one limitation sentence: the findings are conditional on this learner class, state and budget; no optimality of the policy class under SBJTS is claimed.
- **New experiment?** Full generality would require new work, not authorized. A limitation statement suffices for the scoped claim.

### R12 — "The mechanism section mixes objects: T5 uses the full-history conditional mean μ(H_t), the diagnostic measures E[r_t|r_{t−1}], and the policy numbers are at an unstated state. Undefined primitives: CVaR level, horizon, bins."

- **Severity:** MINOR (clarity), but easily fatal for credibility if left.
- **Already answered?** No.
- **Where:** l.137–142, l.169–173.
- **Minimal clarification:**
  - Label the diagnostic as the lag-projected conditional law, a coarsening of μ_S(H_t).
  - State the representative state (t/N=0.5, log(W/W₀)=0, mean over 40 policies).
  - Define the lag bins.
  - State the horizon N and the CVaR level α. α is **not verifiable in the repository** and must come from the frozen protocol.
  - If the executed slopes (−0.674 / +0.015) are quoted, label them as executed-policy local derivatives, never as actor coefficients (−1.56).
- **New experiment?** No.

---

## Objections considered and judged weaker (not in the top 12)

- **Economic magnitude is small.** Δ_W is about 22 bp over the horizon. Answer by reporting relative scale (≈17.5% of Merton mean terminal log wealth; ≈3.7% of Merton CVaR) with a horizon-level, non-annualized caveat.
- **Discrete learner vs continuous-time reference paper.** Answered by the m=λΔt statement.
- **A4 unverified.** Already stated as an assumption (l.111–115).
- **The duplicate TT row removed in pairing.** Disclose in one clause (DEC-RL-004).
