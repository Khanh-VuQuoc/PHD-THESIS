# PMO Manuscript Integration v1

**Date:** 2026-09-22  
**Project:** RL–SBJTS  
**Status:** `MANUSCRIPT_CORE_ASSEMBLED / SCIENTIFIC_BACKBONE_LOCKED`

## 1. What was assembled

The accepted direct comparator, theory coupling package, saved-policy mechanism evidence, and final conditional-law diagnostic have been integrated into a single manuscript narrative:

`training law -> conditional/path structure -> occupancy and continuation values -> learned feedback policy -> wealth and tail-risk outcomes`.

A concise manuscript core is now stored at:

- `rl_sbjts/manuscript/RL_SBJTS_MANUSCRIPT_DRAFT_v1.tex`

A full Vietnamese technical master was also assembled offline from the project reading notes, with Parts XX–XXIII added for the accepted theory, conditional-law mechanism, final evidence chain and source-of-truth map.

## 2. Final main results carried into the manuscript

- FULL: `Delta_W = +0.00220632`, 95% CI `[0.00217262,0.00224227]`; `Delta_CVaR = -0.00318095`, CI `[-0.00336362,-0.00299560]`.
- CAP50: `Delta_W = +0.000554092`, CI `[0.000545001,0.000563736]`; `Delta_CVaR = -0.000761064`, CI `[-0.000810332,-0.000712501]`.
- Policy-level sensitivity using only 40 paired training replications still excludes zero for all four contrasts; favorable sign is 40/40 in every endpoint/constraint pair.
- Mean executed exposure is nearly unchanged across training laws.

## 3. Final mechanism result carried into the manuscript

User T4 conditional-law run:

- 64 blocks x 3,072 paths per law;
- 196,608 paths and 11,599,872 lag pairs per law;
- 4,000 block-bootstrap replications;
- Tesla T4 / CUDA 12.8 / `TORCH_CUDA_FLOAT32_BATCHED`.

Results:

- SBJTS lag slope `-0.125006`, CI `[-0.125843,-0.124150]`;
- SBJTS lag-1 autocorrelation `-0.124750`, CI `[-0.125587,-0.123909]`;
- Merton slope `+0.000135`, CI `[-0.000430,+0.000716]`;
- SBJTS conditional variance reaches `0.0009073` after the most negative lag bin and `0.0004576` after the most positive lag bin versus unconditional about `0.0002623`;
- fixed-Merton 5% tail probability rises to `7.85%` in the most positive SBJTS lag bin while Merton remains approximately flat.

The saved SBJTS FULL policy moves mean risky allocation from about `0.543` at lag `-0.06` to `0.462` at `+0.06`; the Merton-trained policy stays near `0.495–0.496`.

## 4. Theory carried into the manuscript

- T1 exact wealth coupling plus local finite-order expansion;
- T2 low-order moment / one-step marginal matching does not imply RL equivalence;
- T3 trajectory likelihood-ratio gradient under history dependence without assuming the four-feature observation is Markov;
- T4 symmetric occupancy / continuation-value decomposition, explicitly descriptive not causal;
- T5 conditional-information covariance channel;
- entropy time scaling `m = lambda * dt`;
- T3 regularity remains conditional on A4 / A4-mixed.

## 5. Claim discipline

Permanent boundaries retained:

- no universal RL–SBJTS superiority;
- no pure-jump causal attribution;
- no claim that SBJTS is the true market DGP;
- no claim that lagged return alone causes the performance gap;
- no global-optimality claim for the truncated-Gaussian class under SBJTS;
- no claim that the four-feature observation is a complete Markov state;
- the conditional-law diagnostic is descriptive mechanism evidence, not a confirmatory test.

Conditional-mean figures must use within-law deviations, law-specific reference lines, slope or autocorrelation when discussing dependence; raw cross-law level differences must not be attributed solely to temporal dependence because unconditional means are not identical.

## 6. Research stop decision

`STOP EXPERIMENTS` remains binding. No further research-scale execution is open. Remaining work is editorial: broader literature/reference completion, journal-template formatting, language polishing, and advisor/reviewer-driven revisions only.
