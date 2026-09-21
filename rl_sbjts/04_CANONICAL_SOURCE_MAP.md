# 04_CANONICAL_SOURCE_MAP — RL–SBJTS

Updated: 2026-09-21.

## A. Frozen scientific authorities

| Source | Role | Status / identifier |
|---|---|---|
| `BASE4_FINAL_RELEASE_AUDIT.json` | numerical verdict/integrity authority | protocol `c9ef65485a49d40356f3bbb02d491c4b73fcc9ebf0a22f02f64ab87e04a590d4`; backend `TORCH_CUDA_FLOAT32_BATCHED` |
| `BASE4_FINAL_RESULTS_HANDOVER_PMO.md` | PMO-readable final Base 4 handover | estimation-first; confirmatory superiority not claimed |
| `RL_SBJTS_TECHNICAL_IMPLEMENTATION_RECORD_FINAL.md` | implemented data flow, learner and source trace | code-governed implementation record |
| `05B_BASE4_SCIENTIFIC_EXPERIMENT_GPU_RESEARCH_v2_0.ipynb` | Base 4 executed implementation | Drive source ID `1dBsDSYNc6YPW8pxBo_xhwcmMX9ZLVoiF`; GitHub carries a small immutable pointer under `notebooks/frozen/`, while the large executed notebook stays in the frozen Drive research store |
| Base 3 frozen research source | frozen engine + learner definitions loaded by Base 4 | source identity remains pinned by Base 4 ancestry/hashes; do not substitute an older MVP notebook |
| frozen market snapshot | single empirical input consumed by the frozen pipeline | `frozen_market_snapshot_U1_BASELINE_4.npz`, sha256 `7e817762849118fc3abf8d4cf98ad8d65d921fa49cb0d1b3bb34d884b73c5b4a` |

The observed SHA-256 of the downloaded Base 4 notebook bytes on 2026-09-21 is `7bb73be0ddb5ad52534e6d2bdf8829fc2603394188d39f0c337b618fedf97657`. This is a PMO retrieval fingerprint, not a replacement for the protocol's internal ancestry hashes.

## B. Merton / original-paper benchmark facts

The comparator ticket uses the same conceptual benchmark already encoded in Base 1:

- horizon `T = 1`;
- `dt = 1/250` in the canonical positive-control setup;
- risky fraction is the action;
- classical Merton fraction under log utility is `(mu-r)/sigma^2`;
- exploratory constrained action law is the Gaussian Merton policy conditioned to the same hard action bounds.

For the **new empirical comparator**, Claude must not simply reuse the canonical `mu=0.08`, `sigma=0.30` values as the main scientific arm. The main RL–Merton arm must be calibrated from the same frozen training slice that feeds the SBJTS environment, with the target holdout excluded.

## C. Empirical GBM calibration contract for the new comparator

Let `r_t` be the same equally weighted risky log increment consumed by the learner and `dt` the same step size/horizon convention. On the frozen training slice only:

```text
sample_mean = mean(r_t)
sample_var  = variance(r_t) using a documented convention
sigma_M^2   = sample_var / dt
mu_M - r_f  = sample_mean / dt + 0.5 * sigma_M^2
```

Use the Base 4 primary risk-free gross convention when constructing the empirical comparator. Record the exact estimator (`ddof`), units, annualisation and transform. No holdout statistic may enter these values.

This formula is the GBM log-return identity, not an extra fitted degree of freedom. Claude must include a unit test that simulated GBM increments reproduce the locked training-slice mean/variance within a predeclared Monte Carlo tolerance before research training starts.

## D. Frozen Base 4 facts relevant to the extension

- `m = 0.01` for the primary Base 4 strata.
- constraints: `LONG_ONLY_FULL` and `LONG_ONLY_CAP50`.
- learner: linear actor -> truncated-Gaussian policy; linear ridge critic; Adam.
- training budget: 400 updates, 512 paths/update.
- target holdout evaluation: 20 holdout streams x 15 evaluation seeds, 600 paths per evaluation attempt.
- state: `(1, t/N, log(W_t/W_0), r_{t-1})`.
- existing target/control comparison used common-random-number pairing.

## E. Source conflict rule

If narrative and executable code disagree, executed/frozen source wins. If the new comparator needs an implementation detail that cannot be recovered from the frozen sources, Claude must stop and report the missing dependency rather than inventing a standard RL convention.

Do not use `ARTICLE_SBTS` deep-hedging code as a substitute: that repository studies a different paper, network, loss and multi-asset hedging problem.
