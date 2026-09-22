# PMO Conditional-Law Result Audit v1

**Date:** 2026-09-22  
**Ticket:** `C-RLSBJTS-CONDLAW-DIAG-01`  
**Code lineage:** accepted notebook commit `c47304ceadc18fc73db087de15718a9a0abff0c3`  
**Execution owner:** user / paid Google Colab  
**Verdict:** `RESEARCH_EVIDENCE_ACCEPTED_WITH_SCOPE / STOP_EXPERIMENTS`

## 1. Gate audit

The authorized RESEARCH run completed the frozen budget exactly:

- `RUN_MODE = RESEARCH`;
- backend `TORCH_CUDA_FLOAT32_BATCHED`;
- NVIDIA Tesla T4, CUDA available, capability 7.5;
- 64 SBJTS blocks and 64 empirical-Merton blocks;
- 3,072 paths per block;
- 196,608 paths per law;
- 11,599,872 lagged-return pairs per law;
- 4,000 block-bootstrap replications;
- no replacement seeds and no policy training/evaluation.

`simulation_attempts.csv` contains block indices 0--63 for both laws and every attempt is `resumed=False`. The RESEARCH evidence directory contains the expected summary tables plus the per-block checkpoints.

Source provenance matches the frozen lineage:

- Base-3 code concat `db500333b57ae9029bde99018877580978f3c0344567fa8f86b9c74ac788b26e`;
- snapshot `7e817762849118fc3abf8d4cf98ad8d65d921fa49cb0d1b3bb34d884b73c5b4a`;
- training slice `09811db465da1443b092f6b5e18a78b2fe1dda1fbf1709061395b0ed0e72bf01`;
- environment fingerprint `63ba37cc4a26b48b497e424cdeef4981684c1aef1176f2db571efa6e8e48a060`.

The diagnostic artifacts are correctly stamped `C-RLSBJTS-CONDLAW-DIAG-01`, `EXPLORATORY_MECHANISM_ONLY`, `USER_COLAB_RESEARCH_EVIDENCE`.

## 2. Merton control

The iid empirical-Merton control behaves as required.

- RESEARCH lag slope: `+0.0001347`, block-bootstrap 95% interval `[-0.0004298, +0.0007155]`;
- lag-1 autocorrelation: `+0.0001346`, interval `[-0.0004297,+0.0007155]`;
- unconditional mean `0.00027673`, interval includes the frozen calibration mean `m1=0.00027943`;
- unconditional variance `0.000172661`, essentially equal to frozen `v1=0.000172679`;
- conditional variance is flat across the eight bins near `0.0001726--0.0001732`;
- fixed Merton 5% left-tail probability stays near 5% in every bin.

The notebook's independent simultaneous flatness positive control also passes. Therefore the diagnostic does not manufacture lag dependence under an iid law.

## 3. SBJTS conditional-law result

The frozen SBJTS law shows strong lag-dependent conditional structure.

Global descriptive dependence:

- lag slope `-0.125006`, 95% block-bootstrap interval `[-0.125843,-0.124150]`;
- lag-1 autocorrelation `-0.124750`, interval `[-0.125587,-0.123909]`.

The conditional-mean curve is strongly mean-reverting. Selected bins:

| lag bin | mean lagged return | E[r_t | bin] | deviation from SBJTS unconditional mean |
|---|---:|---:|---:|
| `(-inf,-2]` | `-0.05335` | `+0.009792` | `+0.009419` |
| `(-2,-1]` | `-0.01741` | `+0.003414` | `+0.003041` |
| `(-0.5,0]` | `-0.00287` | `+0.000503` | `+0.000129` |
| `(0,0.5]` | `+0.00346` | `-0.000443` | `-0.000817` |
| `(1,2]` | `+0.01773` | `-0.001783` | `-0.002156` |
| `(2,inf)` | `+0.05570` | `-0.002190` | `-0.002563` |

All listed deviations have block-bootstrap intervals that preserve their sign.

Interpretation must use within-law deviations/slopes rather than raw SBJTS-versus-Merton level differences, because the two laws do not have identical unconditional means in this direct comparator calibration.

## 4. State-dependent risk result

The mechanism is not only conditional mean.

SBJTS conditional variance changes strongly with lag state:

- unconditional variance `0.000262257`;
- after the most negative lag bin: `0.000907299` (about 3.5x unconditional);
- after the most positive lag bin: `0.000457573` (about 1.7x unconditional);
- interior bins are around `0.000226--0.000241`.

Using the fixed empirical-Merton 5% loss threshold, SBJTS left-tail probability also changes materially:

- extreme negative lag: `3.19%`;
- `(0,0.5]`: `3.61%`;
- `(1,2]`: `4.72%`;
- extreme positive lag: `7.85%`.

Thus the frozen target law contains state-dependent mean, variance and tail structure. Merton remains flat in all three diagnostics.

## 5. Link to the learned policy

The accepted saved-policy response is qualitatively aligned with the target conditional law:

- under large negative lagged returns, SBJTS expected next return is positive and the SBJTS-trained policy increases risky exposure;
- under large positive lagged returns, SBJTS expected next return becomes negative and the SBJTS-trained policy reduces risky exposure;
- the empirical-Merton-trained policy remains nearly flat in lagged return.

For LONG_ONLY_FULL, the saved mean action moves from about `0.543` at lag `-0.06` to `0.462` at lag `+0.06`; the Merton-trained policy stays near `0.495--0.496` over the same grid. CAP50 shows the same qualitative separation.

This closes the intended descriptive mechanism chain:

`training law -> conditional/path structure -> learned lag feedback -> different deployment outcomes`.

It does **not** identify a causal share of the wealth/CVaR gap attributable solely to lagged return.

## 6. Manuscript-safe claim

A manuscript-safe statement is:

> In the frozen target simulator, the projected risky return exhibits pronounced lag-dependent conditional mean, variance and left-tail risk, whereas the matched empirical-Merton law is flat by construction and is recovered as flat in the simulation control. The SBJTS-trained policies exhibit feedback to lagged return in a direction qualitatively consistent with this target-law structure, while Merton-trained policies are nearly insensitive to the lagged-return state. This is descriptive mechanism evidence, not causal attribution of the performance gap to a single state variable.

Do not claim universal RL-SBJTS superiority, pure-jump causality, external-market validity, or that lagged return alone causes the accepted wealth/CVaR improvement.

## 7. Evidence locations on Drive

Research folder: `conditional_law_v1/evidence/conditional_law_v1/research/`.

Key Drive IDs at audit time:

- `law_summary.json`: `1-W4ASYBeCpwtJJ99XrCeCLsDAEYEIvYJ`
- `conditional_mean_bins.csv`: `166nsC5XmzynMuObhyqcj38pzxGEKA7Ns`
- `conditional_variance_bins.csv`: `1pSbHhfUSVpqi4vX0a8Gi5AxllHg4G5jt`
- `tail_probability_bins.csv`: `1TbrrpCq_sZLbNn5vHJ7ut1hFqZW2hIXJ`
- `simulation_attempts.csv`: `1BS6Al5RBxkPWfc9KoLXRHx-Py0GDEQVa`
- `hardware_manifest.json`: `1YnrgC5L80XlDq9P0htaXHNQDDml4_8Vu`
- `source_fingerprint.json`: `1blphVFRWMr6IVenMVQxERbiUx2UZi3g0`
- `policy_overlay.csv`: `1Hvap0-sB6I9j5tlgJ1aKMAdtlxljFjzA`
- `blocks/`: `13k5XDhf3dZzg0dPDhki2Bcoroq9au0hm`

## 8. PMO decision

The conditional-law mechanism experiment has achieved its scientific purpose. No lag-ablation retraining or additional research-scale experiment is opened.

**STOP EXPERIMENTS. Move to manuscript integration, figures/tables, and final claim/limitation editing.**
