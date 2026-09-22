# Expected RESEARCH outputs — `conditional_law_v1`

**Ticket:** `C-RLSBJTS-CONDLAW-DIAG-01`
**Claim status:** `EXPLORATORY_MECHANISM_ONLY`
**Executed by:** the user, on the paid Colab NVIDIA T4, only after PMO authorises the
budget. Claude has not run and must not run RESEARCH mode.

This directory is **empty until that authorised run happens**. Nothing Claude produced
belongs here; Claude's artifacts live in `../smoke/` and are not scientific evidence.

## Proposed bounded budget

| Field | Value |
|---|---|
| Blocks per law | 64 |
| Paths per block | 3,072 |
| Paths per law | 196,608 |
| Decision steps per path | 60 (frozen `N_STEPS`) |
| Lagged pairs per law | 11,599,872 |
| Bootstrap replicates | 4,000 |
| Resampling unit | simulation seed block (64 units) |

Blocks are favoured over paths-per-block on purpose. Uncertainty is quantified at the
block level, so 64 resampling units of 3,072 paths is a
better design than half as many units of twice the size at identical cost.

### Why this is enough

The narrowest bins are the two tails, which hold roughly 2% of pairs each, so about
231,997 pairs. At the observed SBJTS one-step dispersion (sd ~ 0.0162) the
row-level standard error of a tail-bin conditional mean is about
3.4e-05. The smoke run measured a block-bootstrap interval
about 1.35x wider than a row-iid interval, so budget for roughly
4.5e-05 in the tails and appreciably finer in the
six interior bins. That resolves conditional-mean deviations of order 1e-4, which is the
scale the smoke fixture showed.

### Estimated runtime and footprint

Measured on this CPU sandbox under `TORCH_CPU_FLOAT32_BATCHED`, by timing the frozen
engine at two path counts:

| Probe | Paths | Elapsed |
|---|---|---|
| 1 | 128 | 0.58 s |
| 2 | 512 | 1.75 s |

Fitting `elapsed ~= fixed + marginal * n_paths` gives a marginal cost of about
3.41 ms per path. At the proposed budget:

- SBJTS simulation: about **11 minutes**;
- Merton control: seconds (pure NumPy);
- bootstrap and sup-statistic: a few minutes, since they operate on sufficient
  statistics rather than raw pairs;
- **end-to-end allowance: 45 minutes** on one T4 session, which leaves ample headroom.

Peak resident memory scaled linearly in the smoke probes: about +280 MB above a ~615 MB
baseline at 4,096 paths per block, so roughly **0.9 GB peak** at 3,072 paths. Comfortable
on a standard Colab T4 instance.

**Honest limitation:** these timings are CPU measurements. Claude has no GPU in this
sandbox and has therefore not measured the `TORCH_CUDA_FLOAT32_BATCHED` path. The T4 run
may be faster or slower; the 45-minute allowance is deliberately loose for that reason.

### Why the T4 is required, scientifically

The accepted comparator lineage ran the frozen engine under
`TORCH_CUDA_FLOAT32_BATCHED`. Characterising the same law under a different numerical
backend would not be the same measurement, so RESEARCH mode hard-requires CUDA on a T4
with no CPU fallback. This is a consistency requirement, not a performance one.

## Expected files

| File | Contents |
|---|---|
| `conditional_mean_bins.csv` | per law and bin: n, mean lagged return, `E[r_t \| bin]`, deviation from that law's unconditional one-step mean, and cluster-bootstrap 95% intervals |
| `conditional_variance_bins.csv` | per law and bin: conditional variance of `r_t` with intervals |
| `tail_probability_bins.csv` | per law and bin: `P(r_t <= q_0.05^M \| bin)` against the fixed Merton 5% one-step quantile, with intervals |
| `law_summary.json` | binning scheme and edge convention, frozen constants, per-law unconditional moments, lagged-return slope, lag-1 autocovariance and autocorrelation, bootstrap metadata, source fingerprint |
| `simulation_attempts.csv` | one row per (law, block): seed, paths, steps, elapsed seconds, whether the block was resumed from a checkpoint |
| `hardware_manifest.json` | device, CUDA and torch versions, backend actually used |
| `source_fingerprint.json` | Base 3 code-concat digest, snapshot and training-slice digests, environment fingerprint, frozen Merton calibration |
| `policy_overlay.csv` | direction-only join of the conditional-mean curve with the already-accepted policy response on the lagged-return axis |
| `blocks/` | per-(law, block) sufficient-statistic checkpoints; the resume unit |

### Manuscript-ready figure specification

**Figure — conditional-mean response to the lagged return, by training law.**
x axis: the eight fixed `z_{t-1}` bins, plotted at each bin's observed mean lagged
return. y axis: `E[r_t \| bin]` in per-step log-return units. Two series: SBJTS target and
empirical Merton/GBM, each with cluster-bootstrap 95% bands and a dashed horizontal line
at that law's unconditional one-step mean. Annotate each bin with its n. The Merton
series is the control and should lie on its dashed line; a visibly sloped SBJTS series
would indicate lag-dependent conditional structure in the training law.

**Table — law summary.** Per law: unconditional one-step mean and variance, the
descriptive lagged-return slope with its block-bootstrap interval, the lag-1
autocorrelation with its interval, and n pairs. One footnote must state that both laws
are binned on the frozen Merton scale, so differing bin occupancy reflects differing
one-step dispersion and is not itself evidence of conditional structure.

## Acceptance checks that must accompany the run

The notebook runs the Merton flatness positive control in both modes and **raises** if
the iid arm does not come back flat. A RESEARCH run that reports results without that
control having passed should be rejected.

## Claim discipline

Whatever the curve looks like, this diagnostic does not establish that the lagged-return
coordinate causes the RL–SBJTS performance advantage, does not isolate a pure jump
effect, does not demonstrate external market validity, and is not a confirmatory test.
It characterises two market laws.
