# RL–SBJTS final editorial patch plan v1

**Date:** 2026-09-28  
**Target:** `manuscript/RL_SBJTS_MANUSCRIPT_DRAFT_v1.tex` at `main` = `6ddb4a5`  
**Status of this plan:** proposed; **nothing is applied** until PMO reviews it.  
**Constraints:** no experiment, no retraining, no estimand change, no change to accepted results, scope or claim boundaries. Every item is wording, disclosure or citation.  
**Basis:** `RL_SBJTS_FINAL_CLAIM_REFERENCE_AUDIT_v1.md` (row IDs in brackets) and `RL_SBJTS_REVIEWER_ATTACKS_v1.md` (R-numbers).

Items marked **[PMO decision]** need a PMO choice before they can be drafted.

---

## P0 — scientific correctness / overclaim

| ID | Location | Change | Why |
|---|---|---|---|
| P0-1 | Conclusion l.179 | Replace "…even when local low-order return moments are matched" with "…; the theory shows that matching local low-order moments is not sufficient in general." (Use the alternative only if P0-2 option (b) is adopted.) | [C3], R2. The direct comparator is not moment-matched to the deployment law. |
| P0-2 | Intro l.27 and Design l.53 | Add one sentence: the GBM is calibrated to the historical training slice, not to the simulator's moments, so the comparator measures the cost of the standard diffusion calibration. **[PMO decision]** also add (b) a short Base 4 paragraph reporting the moment-matched no-jump control (diagonal variance ratio 0.996 vs terminal 1.274; FULL Δ_W ≈ +3.81×10⁻⁴, Δ_CVaR ≈ −6.14×10⁻⁴), with numbers confirmed against the frozen Base 4 handover first. | [I2], R2. |
| P0-3 | Design l.53 | State that the SBJTS arm trains on the deployment law with disjoint seeds (an oracle-law reference), and frame the contribution as quantifying the cost of the data-calibrated diffusion law. | [D7], R1. |
| P0-4 | Objective l.42 | Move the entropy sum inside the expectation: `E_θ[ log(W_T/W_0) + m Σ_{t=0}^{N-1} H(λ_θ(·|S_t)) ]`. | [B4]; consistency with l.102. |
| P0-5 | Abstract l.23 | Make three wording changes: (a) "jump-rich" → "with jump and temporal-dependence components"; (b) "is not explained by average risky exposure" → "is not accompanied by a material difference in average executed risky exposure"; (c) "decomposes market-law effects through …" → "organizes how the training law enters the problem through exact wealth coupling and a gradient-gap identity with occupancy, continuation-value and entropy terms (an attribution convention, not a causal decomposition)". | [AB1], [AB7], [AB9]. |
| P0-6 | Mechanism l.169 | Name the estimand: "slope of r_t on r_{t−1}, summarizing the lag-projected conditional mean E_S[r_t|r_{t−1}], a coarsening of the full-history μ_S(H_t) in §Theory". | [M3], R12; full-history vs lag-projected distinction. |
| P0-7 | Mechanism l.173 | Add "at the representative state t/N=0.5, log(W_t/W_0)=0, averaged over the 40 saved policies". If slopes are added, label them "local derivative of the executed mean action" (FULL −0.674 vs +0.015). Never quote the raw coefficient −1.56. | [M6], [M8]; supersession note §E. |
| P0-8 | T5 l.142 | "and its absence under the iid law" → "and the vanishing of this conditional-mean covariance term under the iid law". | [T5b]; PMO theory-patch audit §4. |
| P0-9 | Discussion l.176 | Add the missing permanent limitations: (a) SBJTS calibration ancestry is limited-scale, so no historical-market validity is claimed; (b) estimation-first, with no prespecified smallest effect size, so not a confirmatory test; (c) the GBM arm is data-calibrated, not moment-matched to the deployment law; (d) one learner class, state and exploration level, with no optimality of the truncated-Gaussian class claimed; (e) the T4 channels are not estimated on the frozen problem; (f) a lag-ablation contrast was not run, so the mechanism is directional alignment only. | [L3], R4, R5, R7, R9, R11. |
| P0-10 | Design | Define the missing primitives: horizon N **[PMO confirm N=60]**, CVaR level α **[PMO supply; not in repository]**, "CVaR log loss", holdout structure (20 streams × 15 seeds, 600 paths), common-random-number pairing, the crossed-cluster bootstrap (training replication × holdout block), and the policy-level sensitivity. Disclose the single duplicate SBJTS row removed before pairing. | [B6], [D5], [D6], R10, R12. |
| P0-11 | Results table l.148–163 | Report CIs at 4 significant figures, or have PMO confirm CAP50 Δ_W CI low from Drive `primary_estimands.json`. The repository snapshot has 0.000544995 and the manuscript 0.000545001; both round to 0.0005450. | Audit B.1 conflict. |
| P0-12 | Mechanism, first sentence of l.169 | Add: "These statistics characterize the frozen target simulator; they are not presented as evidence that conditional dependence of this magnitude holds in historical or future market returns." | PMO scope ruling 2026-09-28; R6. |

## P1 — literature / citation completeness

| ID | Change | Why |
|---|---|---|
| P1-1 | Add `\cite` calls for the three existing references at their first relevant sentences (Merton 1969/1971 at l.27; Chau–Nguyen–Nguyen at the truncated-Gaussian policy l.38 and at l.44). | There are currently zero in-text citations. |
| P1-2 | Complete the existing entries: Merton 1969 DOI 10.2307/1926560; Merton 1971 DOI 10.1016/0022-0531(71)90038-X (confirm); Chau et al. issue 3, author given names and DOI **(DOI not independently resolved; PMO/author to confirm)**. | Audit G. |
| P1-3 | Add the ESSENTIAL references (all verified): Wang–Zariphopoulou–Zhou 2020 (JMLR 21); Gao–Li–Zhou arXiv:2405.16449; Nguyen–Nkuize arXiv:2604.22188; Merton 1976 (JFE 3); Rockafellar–Uryasev 2000 (J. Risk 2(3)); Williams 1992 (ML 8); Baxter–Bartlett 2001 (JAIR 15). Also add **the SBJTS source work [author to supply]**. | Audit D. |
| P1-4 | Add the HIGH VALUE references (verified): Wang–Zhou 2020 (Math. Finance 30(4)); Jia–Zhou 2022 (JMLR 23); Cvitanić–Karatzas 1992; Nilim–El Ghaoui 2005 and/or Iyengar 2005; Tamar–Glassner–Mannor 2015; Hambly–Xu–Yang 2023. Add Hawkes 1971 and Aït-Sahalia–Cacho-Diaz–Laeven 2015 **only if** SBJTS intensity is self-exciting (author to confirm). Add Lo–MacKinlay 1988 if Base 4 is reported. | Audit D. |
| P1-5 | Do **not** add Sutton et al. 2000 or any OPTIONAL item until verified or needed. | Audit D.6; do not inflate the bibliography. |
| P1-6 | Place the citations: T3 (Williams; Baxter–Bartlett) at l.89; entropy/exploratory formulation (Wang–Zariphopoulou–Zhou) at l.44; CVaR (Rockafellar–Uryasev) at the endpoint definition; jump-diffusion (Merton 1976; Gao–Li–Zhou) in the Intro; misspecification (robust MDP) in the Intro/Discussion. | Each citation must support the sentence it sits on. |

## P2 — narrative clarity / novelty positioning

| ID | Change | Why |
|---|---|---|
| P2-1 | Add a short related-work paragraph and the 3-bullet contribution statement (audit §E.4) to the Introduction. Distinguish the paper from Chau–Nguyen–Nguyen (analytic GBM optimum), Nguyen–Nkuize (analytic stochastic-volatility optimum), Gao–Li–Zhou (jump-diffusion RL algorithms) and CVaR-optimizing RL (this paper evaluates CVaR, it does not optimize it). | Audit §E; R1, R8. |
| P2-2 | Add an SBJTS model section or appendix from the frozen technical record; expand the acronym **[author to supply]**; add a data/code availability statement with the frozen hashes. | R3. |
| P2-3 | Position T3/T4 as framework results with precedents cited; state that T4 is verified on an enumerable model and is not estimated on the frozen experiment; add a proof sketch or appendix for the T2 proposition, using the derivative statement for T2b. | [T2a], [T4a], R8, R9. |
| P2-4 | State λ_equiv = m/Δt = 2.5 at l.44 and note that both arms' mean actions sit near the interval centres. | [B5], R4. |
| P2-5 | Add one sentence on economic scale: horizon-level Δ_W ≈ 22 bp (≈17.5% of the Merton arm's mean terminal log wealth); Δ_CVaR ≈ 3.7% of Merton CVaR; CAP50 effects ≈ 25% of FULL. | [R4], [R5]. |
| P2-6 | Define the lag bins (units/standardization) **[PMO to confirm from the diagnostic spec]**. Optionally add the exact extreme-negative-bin tail probability of 3.19%. Use "2.8–3.2%" only if marked as rounded. | [M4], [M5]. |
| P2-7 | **Withdrawn** (PMO scope ruling 2026-09-28). No training-slice autocorrelation statistic is reported; the diagnostic is scoped to the simulator and P0-12 states this. | R6. |

## P3 — language / style / formatting

| ID | Change |
|---|---|
| P3-1 | Replace the author placeholder at l.17. |
| P3-2 | Use one rounding convention: 4 significant figures for effects and CIs in the abstract and text; the table may carry 6. |
| P3-3 | Rename the entropy temperature (e.g. γ) to avoid a clash with the policy density λ_θ. |
| P3-4 | In T3, define ψ_θ and R^soft before they are used in (A4). |
| P3-5 | Remove internal jargon from reader-facing text: "user-run", "frozen … rows are reused", "Base 4", "TT/MT", "locked research record". Keep "frozen" only where it means pre-specified and immutable. |
| P3-6 | Replace LONG\_ONLY\_FULL / LONG\_ONLY\_CAP50 with named constraints (e.g. "long-only" and "50% cap") after first definition. |
| P3-7 | Number all theory results consistently (Proposition 1–5 or Lemma/Proposition), rather than one numbered proposition among unnumbered prose results. |
| P3-8 | Journal-template adaptation, figures (forest plot of the four contrasts; conditional-law and policy-response panels from existing CSVs) — after P0–P2. |

---

## Items explicitly **not** proposed

- Any new training, evaluation, bootstrap, lag-ablation, exploration sweep, moment-matched GBM retraining or historical backtest.
- Any change to accepted numbers, estimands or claim status.
- Any edit to `reports/claude/RL_SBJTS_THEORY_COUPLING_v1.md` or frozen evidence.

## Decisions needed from PMO

1. P0-2(b): report Base 4 in the manuscript (numbers to be confirmed against the Base 4 handover), or rely on T2 alone.
2. P0-10: confirm horizon N = 60 and supply the CVaR level α.
3. P0-11: confirm CAP50 CI digits from Drive, or accept 4-significant-figure reporting.
4. P2-2: SBJTS acronym, model reference and appendix source.
5. P2-6: lag-bin units.
6. ~~P2-7~~ resolved by the 2026-09-28 scope ruling (P0-12); no statistic is reported.
