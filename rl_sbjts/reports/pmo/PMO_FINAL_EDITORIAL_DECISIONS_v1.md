# PMO final editorial decisions v1

**Date:** 2026-09-28  
**Status:** `FINAL_EDITORIAL_PATCH_AUTHORIZED`  
**Scope:** editorial/manuscript patch only. No new training, evaluation, bootstrap, ablation, historical backtest, or change to accepted estimands/results is authorized.

This note resolves the open PMO questions in `RL_SBJTS_FINAL_PATCH_PLAN_v1.md` and is authoritative for the final manuscript patch.

## 1. Base 4: include it, but keep it separate from the direct Merton comparator

**Decision: INCLUDE.**

Base 4 is an earlier auxiliary within-family control that approximately matches the canonical one-step mean and variance between the SBJTS target law and the corrected no-jump affine control. It is **not** the direct empirical Merton/GBM comparator.

Manuscript-safe Base 4 numbers, confirmed against `reports/research/RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md` and the accepted Base 4 handoff:

- LONG_ONLY_FULL: `Delta_W = +3.809735e-4`, 95% interval approximately `[+3.6190e-4,+4.0079e-4]`;
- LONG_ONLY_FULL: `Delta_CVaR = -6.137117e-4`, 95% interval approximately `[-6.6569e-4,-5.6428e-4]`;
- diagonal/time-local variance ratio `0.996409`, 95% interval `[0.989078,1.004246]`;
- terminal variance ratio `1.274346`, 95% interval `[1.254713,1.292400]`;
- the variance decomposition identity was verified on 20/20 validation seeds, maximum numerical error `1.39e-17`.

Use Base 4 only to support the empirical statement that approximate local first-two-moment matching did not remove the path/terminal-law difference and did not make the learned-policy problem empirically equivalent. Do not use it as a causal decomposition of a jump effect.

The direct comparator must instead be described as an empirical Merton/GBM law calibrated to the frozen historical training slice, **not** moment-matched to the SBJTS deployment law.

## 2. Horizon

**Decision: `N = 60` decision steps per path.**

This is the frozen `N_STEPS` used by the research environment. With `dt = 1/250`, the simulated decision horizon is `60/250` years under the frozen discrete convention. Do not silently replace it by `N=250` merely because the Base 1 pedagogical benchmark uses a one-year 250-step grid.

## 3. CVaR definition and level

**Decision: `alpha = 0.95`.**

This value was resolved by static inspection of the exact frozen Base-3 source consumed by Base 4, not by convention or inference.

Provenance chain:

- canonical Base-3 frozen ZIP: `BASE3_FROZEN_0c0d95cf7cfba366c4ed9e7e2ed09969fa459f933e08ff6422a5153e6495223f.zip`;
- Google Drive file ID: `13_rStM-xLtvEDN7btI-0snY1yP_bw-_O`;
- ZIP SHA-256: `d3e77de4ae40fdbde31b607105c31f95d07033d00abd2bd71f93d9f3cdad0f63`;
- embedded source: `03_RL_SBJTS_RESEARCH_GPU_HYBRID_v1_8.ipynb`;
- embedded-source SHA-256: `344956031d9e89763370a020d92ec54a669a7cc400e3d2b674de613897c02129`;
- frozen source sets `TAIL_ALPHA = 0.95`.

The frozen loss convention is

`terminal_log_loss = -log(W_T/W_0)`.

The frozen `tail_metrics` implementation uses:

- `VaR_alpha`: empirical `alpha`-quantile of terminal log loss;
- `CVaR_alpha`: mean terminal log loss among observations with loss `>= VaR_alpha`.

Therefore `cvar_log_loss` in the accepted experiment is the empirical `CVaR_0.95` of positive terminal log loss, i.e. the average loss in the upper 5% tail under the frozen empirical convention.

Do not confuse this `0.95` with the 95% confidence intervals used for effect estimates or with the fixed Merton 5% return threshold in the conditional-law diagnostic.

## 4. SBJTS name and external source

**Decision:** expand SBJTS on first use as **Schrödinger Bridge with Jumps for Time Series (SBJTS)**.

Primary source to cite:

Stefano De Marco, Huyên Pham, and Davide Zanni (2026), *Schrödinger bridges with jumps for time series generation*, arXiv:2602.20011.

The source introduces a jump-diffusion Schrödinger-bridge framework for time-series generation, with data-driven controlled drift and jump intensity. The manuscript must separately describe the **frozen project implementation/adaptation** and must not imply that every implementation detail in the frozen simulator is a theorem or specification copied verbatim from the source paper.

## 5. Lag-bin units

**Decision:** the conditional-law bins are in **Merton-standardized lag z-score units**, not raw-return units.

For both laws,

`z_{t-1} = (r_{t-1} - m1) / sqrt(v1)`,

using the frozen empirical Merton one-step calibration. The common fixed right-closed bins are:

`(-inf,-2], (-2,-1], (-1,-0.5], (-0.5,0], (0,0.5], (0.5,1], (1,2], (2,inf)`.

If a table reports a `mean_lagged_return` such as `-0.05335`, label it as the mean **raw lagged return within that standardized bin**; it is not a bin edge.

## 6. CAP50 confidence-interval precision

**Decision:** use a common manuscript rounding convention rather than chasing unsupported extra digits.

For the CAP50 wealth contrast, report the crossed interval in prose/summary as approximately

`[0.0005450, 0.0005637]`.

The repository snapshot and a higher-precision artifact differ only beyond the meaningful reporting precision. Do not present false precision.

## 7. Historical lag-1 autocorrelation

**Decision: DO NOT ADD.**

Do not compute or report a post-hoc historical training-slice autocorrelation merely to contextualize the simulator's `-0.125` value. The manuscript should state instead that the conditional-law diagnostic characterizes the frozen target simulator and is not evidence that conditional dependence of the same magnitude holds in historical or future markets.

## 8. Reviewer/audit reports

The final read-only Claude audit reports are accepted as editorial input:

- `reports/claude/RL_SBJTS_FINAL_CLAIM_REFERENCE_AUDIT_v1.md`;
- `reports/claude/RL_SBJTS_REVIEWER_ATTACKS_v1.md`;
- `reports/claude/RL_SBJTS_FINAL_PATCH_PLAN_v1.md`.

They have been merged to `main` before this decision note. They do not change accepted research evidence.

## 9. Final patch instruction

The next Claude action may edit the manuscript only. It should implement the accepted P0/P1/P2/P3 editorial changes using the decisions above, compile the TeX, report the exact diff, and stop at `READY_FOR_PMO_FINAL_EDITORIAL_PATCH_AUDIT`.

Permanent scope remains: no universal SBJTS superiority, no pure-jump causal attribution, no lag-alone causal attribution, no historical-market validity claim, no global optimality claim for the truncated-Gaussian policy class, and no confirmatory-superiority claim.