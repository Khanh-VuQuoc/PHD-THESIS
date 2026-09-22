# RL–SBJTS conditional-law mechanism diagnostic — code and smoke package

**Ticket:** `C-RLSBJTS-CONDLAW-DIAG-01`  
**Status:** `READY_FOR_PMO_CODE` — design, implementation and smoke only.  
**Revision:** second submission, patching commit `e60a351` per `reports/pmo/PMO_CONDLAW_CODE_AUDIT_v1.md` (P1 provenance, P2 dependencies). The estimand, bins, block-bootstrap design, controls, research budget and claim discipline are unchanged.  
**Claim status:** `EXPLORATORY_MECHANISM_ONLY`.  
**Policy training or evaluation:** none. Market simulation only, enforced by a static AST gate.  
**Generated:** 2026-09-22T06:33:51.025239+00:00 · smoke package runs in 8.9 s on CPU.

RESEARCH mode has **not** been run and cannot be run here: it hard-requires a CUDA NVIDIA T4, and this sandbox has no GPU. The proposed budget is in §6.

## 0. Patch response (PMO code audit v1)

Both findings were correct, and both came from reusing comparator scaffolding wholesale rather than from the diagnostic's own design. Nothing scientific changed.

| patch | finding | fix |
|---|---|---|
| **P1** | diagnostic artifacts were stamped with the comparator ticket and carried comparator-specific claim wording | The package no longer writes through `comparator_config`. A new `condlaw_config` owns the stamp: every artifact carries `ticket`, `producing_ticket` and `diagnostic_id` all equal to `C-RLSBJTS-CONDLAW-DIAG-01`, plus `claim_status = EXPLORATORY_MECHANISM_ONLY`, and a caller payload cannot overwrite those fields. The comparator's "never report as comparator evidence" wording is gone, replaced by a diagnostic-specific smoke note. The notebook's hardware cell was also writing through the comparator stamper and now does not. |
| **P2** | the notebook staged `policies.npz`, `training_attempts.csv` and the 31 MB evaluation ledger, the last resolved by largest-file-if-ambiguous | Step 00 is rewritten. It stages exactly two inputs, each content-pinned and each labelled with the function that executes it. There is no largest-file fallback anywhere: `resolve` accepts a candidate only on a digest match. The two accepted compact policy tables are carried inline in the notebook (about 3.8 kB) with their source digests verified on write, so the overlay needs no Drive lookup at all. Step 00 raises if a not-required artifact is staged anyway. |

Two new gates enforce the fixes, and both are shown to bite:

- **`S12`** scans every generated artifact (21 of them) for the producer keys and for any stray comparator ticket string. A comparator ticket is permitted **only** under an explicitly labelled input-provenance key, because the policy-response tables genuinely were produced by that ticket and saying so is correct attribution. Its negative control stamps an artifact through `comparator_config.stamp`, the actual pre-patch code path, and confirms the scan flags it: `True`, 1 offence and 3 missing stamps detected.
- **`S13`** checks the dependency claim two ways: statically, that no module on the diagnostic path names a not-required artifact outside the declaration itself (`0` hits); and behaviourally, that the overlay — the only consumer of comparator evidence — builds correctly with **only** the two pinned compact tables present in its search path (`True`, 20 rows from 2 files).

**Executed inputs, and what is deliberately absent.** Simulating two market laws and binning their lagged pairs needs neither saved policies nor any ledger:

| input | executed by | why |
|---|---|---|
| `03_RL_SBJTS_RESEARCH_GPU_HYBRID_v1_8.ipynb` | `frozen_loader.load_base3_namespace / verify_native_ast_hashes` | supplies the frozen market engine and calibration code that Base4Engine.make_base4_market_pair executes |
| `frozen_market_snapshot_U1_BASELINE_4.npz` | `frozen_loader.build_frozen_environment` | supplies the frozen calibration inputs and the training slice the empirical Merton one-step calibration is fitted to |

Not staged, by design: `policies.npz`, `training_attempts.csv`, `evaluation_results_partial.csv`, `evaluation_results.csv`, `BASE4_05A_FINAL_BUNDLE.zip`.

## 1. What the diagnostic asks

Whether the frozen SBJTS target law contains lag-dependent conditional structure, $\mu_L(H_t)=E_L[r_t\mid H_t]$, that the empirical iid Merton/GBM comparator cannot contain by construction. Under an iid law the conditional mean is a constant, so the response curve is flat by definition; any departure under SBJTS is a property of the training law.

This is a statement about two market laws. It is **not** a causal decomposition of the RL performance gap. §7 states the restrictions in full.

## 2. Frozen sources

- Base 3 code-cell concat `db500333b57ae902…` (matches pinned: `True`)
- Market snapshot `7e817762849118fc…`, training slice `09811db465da1443…` (matches pinned: `True`)
- Environment fingerprint `63ba37cc4a26b48b…`, `N_STEPS=60`, `N_PI=5`, `dt=0.004`
- Frozen empirical Merton calibration: `m1 = 0.0002794269605`, `v1 = 0.0001726791907`, `sigma_M = 0.2077734286933`, `mu_M - r_f = 0.09144163895549`

Both laws are sampled as the **same market object**: project_ew(inc): equally weighted log increment over the four snapshot assets, the same object the learner consumes and the same object the Merton arm was calibrated to. That matters — comparing a different projection between arms would make the two curves incomparable before any statistics were done.

## 3. Design

### 3.1 Estimand and binning

Pairs $(r_{t-1},r_t)$ are collected for every decision time after the first lag is available and never across a path boundary. Lagged returns are standardised with the frozen Merton one-step calibration, $z_{t-1}=(r_{t-1}-m_1)/\sqrt{v_1}$, and the same standardisation and the same fixed bins are applied to both laws:

```text
(-inf,-2], (-2,-1], (-1,-0.5], (-0.5,0], (0,0.5], (0.5,1], (1,2], (2,inf)
```

Bins are **right-closed**: a value exactly on an edge falls in the lower bin. Verified explicitly (check `S1`), because an undeclared edge convention is the kind of thing that silently differs between two implementations.

A consequence worth stating in the manuscript: because both laws are binned on the *Merton* scale, bin occupancy differs whenever their one-step dispersions differ. In the smoke fixture the SBJTS law has the larger dispersion (2.626e-04 versus 1.747e-04), so it puts more mass in the outer bins. **Differing bin counts are not evidence of conditional structure**; only the within-bin response is.

### 3.2 Block sufficient statistics

Every reported quantity is a function of per-(law, block, bin) sufficient statistics: counts, $\sum r_{t-1}$, $\sum r_t$, $\sum r_t^2$, tail counts, and the pair sums needed for the slope and autocorrelation. This one choice buys three things at once:

1. **Resumability.** Each (law, block) writes its own checkpoint atomically; a resumed run recombines checkpoints instead of re-simulating.
2. **Exactness.** Pooling is addition in block-index order, so a resumed run reproduces an uninterrupted one bit for bit (check `S6`).
3. **A cheap cluster bootstrap.** Resampling blocks means re-adding small arrays, not re-touching millions of pairs.

### 3.3 Uncertainty at the block level

The resampling unit is the simulation seed block, as the ticket requires. Returns within a path are dependent by construction under the very law being tested, so a row-iid interval would understate uncertainty. Check `S7` quantifies this rather than asserting it: on the smoke fixture the block-bootstrap slope interval is 1.35× the width of the row-iid interval, and the bootstrap refuses to run at all on a single block.

### 3.4 Seed isolation

Diagnostic blocks draw from their own seed namespaces. The check is numeric, not nominal: all 128 diagnostic seeds are compared against all 720 Base 4 training and holdout seeds, and the intersection is empty. Reusing a holdout market seed would entangle a descriptive diagnostic with the frozen evaluation sample.

## 4. The flatness control, and a method correction

The iid Merton arm is the positive control: its conditional-mean curve must come back flat, and the notebook **raises** in both modes if it does not.

My first implementation read eight per-bin 95% intervals and required all of them to cover $m_1$. That is a multiplicity error, and it duly failed on honest iid data: with eight bins, at least one miss has probability about $1-0.95^8\approx34\%$ even under a perfectly flat law. Bonferroni-adjusting the intervals fixes the level but pushes the required bootstrap percentile out to 0.3%, which a few dozen blocks cannot resolve stably.

The package therefore uses a **simultaneous studentized sup-statistic**, which asks the simultaneous question directly and only ever needs a central percentile of the bootstrap distribution:

$$ T=\max_i\frac{|\hat\mu_i-m_1|}{\hat{se}_i},\qquad T^*_b=\max_i\frac{|\hat\mu^*_i(b)-\hat\mu_i|}{\hat{se}_i},\qquad \text{flat}\iff T\le Q_{0.95}(T^*). $$

| control | statistic | critical value | verdict |
|---|---|---|---|
| Merton iid (positive control) | 1.057 | 2.696 | flat: `True` |
| AR(1) injected, ρ=0.15 (negative control) | 42.563 | 2.710 | flat: `False` |

The same gate that passes on iid data fails decisively on a mild injected AR(1) (42.6 against a critical value of 2.71), and the AR(1) slope interval [0.1456, 0.1524] excludes zero. A flatness check that could not be made to fail would evidence nothing.

Alongside the sup test, the Merton control also satisfies the two global checks: the lagged-return slope interval [-2.80e-03, 2.59e-03] covers zero, the lag-1 autocorrelation interval covers zero, and the pooled left-tail probability is 0.0499 against the nominal 0.05 — confirming the fixed Merton quantile is being applied correctly.

## 5. Smoke results

**13/13 checks pass**, 4 of them controls that must fail or block and do.

| check | what it establishes | pass |
|---|---|---|
| `S1_BIN_SCHEME` | bin edges, right-closed convention, every probe in range | True |
| `S2_SUFFICIENT_STATISTICS_ADDITIVE` | pooling equals computing on the concatenation; counts exact, sums to round-off; no pair crosses a path boundary | True |
| `S3_MERTON_FLAT_CONTROL` | the iid law returns a flat curve under the simultaneous sup test | True |
| `S4_AR1_NEGATIVE_CONTROL` | an injected AR(1) trips the same gate (negative control) | True |
| `S5_PAIRING_NEGATIVE_CONTROL` | destroying the time pairing kills the slope while preserving every one-step marginal exactly (negative control) | True |
| `S6_RESUME_EXACT` | a resumed run reproduces an uninterrupted one exactly | True |
| `S7_CLUSTER_UNIT_IS_THE_BLOCK` | uncertainty is block level; the single-block case is refused | True |
| `S8_NO_ACTOR_TRAINING` | AST scan: no actor, critic or learner-update symbol is referenced | True |
| `S9_SEED_ISOLATION` | diagnostic seeds disjoint from all Base 4 seeds | True |
| `S10_NAMESPACE_ISOLATION` | SMOKE cannot write into research/ and vice versa (negative control) | True |
| `S11_RESEARCH_REQUIRES_NVIDIA_T4` | RESEARCH refuses to run without a T4 (negative control) | True |
| `S12_PRODUCER_TICKET_PROVENANCE` | every artifact names this ticket as producer; a comparator ticket appears only as labelled input provenance (carries its own negative control) | True |
| `S13_NO_RAW_LEDGER_DEPENDENCY` | no policy, training or evaluation ledger is required; the overlay builds from the two pinned compact tables alone | True |

`S5` deserves a note because it is the control that protects the headline quantity. Permuting each step's column independently preserves every one-step marginal exactly (verified: `True`) while removing the time linkage. On the SBJTS fixture the slope moves from -0.1335 to -0.0093. A slope that survived this would have been an artefact of the marginals rather than evidence of conditional structure.

### 5.1 Smoke-scale numbers, which are not evidence

The smoke fixture is 6 blocks × 64 paths per law (22,656 pairs). Its purpose is to exercise every bin and the whole output schema. **The values below are not mechanism evidence and must not be quoted as a finding** — that is exactly what the authorised RESEARCH run is for.

| law | unconditional mean | unconditional variance | lag slope [95% block CI] | lag-1 autocorrelation |
|---|---|---|---|---|
| SBJTS_TARGET | 3.8251e-04 | 2.6264e-04 | -0.1140 [-0.1316, -0.0973] | -0.1140 |
| MERTON_EMPIRICAL_GBM | 4.4283e-04 | 1.7466e-04 | +0.0073 [-0.0124, +0.0238] | +0.0073 |

All eight bins are populated for both laws at this tiny scale:

| bin | SBJTS n | SBJTS `E[r_t \| bin]` | Merton n | Merton `E[r_t \| bin]` |
|---|---|---|---|---|
| `(-inf,-2]` | 493 | +8.358e-03 | 541 | -2.152e-04 |
| `(-2,-1]` | 2,108 | +3.323e-03 | 3,008 | +1.980e-04 |
| `(-1,-0.5]` | 3,199 | +1.480e-03 | 3,324 | +2.190e-04 |
| `(-0.5,0]` | 5,224 | +4.021e-04 | 4,354 | +6.761e-04 |
| `(0,0.5]` | 5,487 | -3.681e-04 | 4,363 | +4.602e-04 |
| `(0.5,1]` | 3,576 | -4.855e-04 | 3,338 | +9.500e-04 |
| `(1,2]` | 2,123 | -2.041e-03 | 3,173 | +1.463e-04 |
| `(2,inf)` | 446 | -2.629e-03 | 555 | +8.776e-04 |

## 6. Proposed bounded RESEARCH budget

| Field | Value |
|---|---|
| Blocks per law | 64 |
| Paths per block | 3,072 |
| Paths per law | 196,608 |
| Lagged pairs per law | 11,599,872 |
| Bootstrap replicates | 4,000 |
| Resampling unit | simulation seed block (64 units) |
| Backend | `TORCH_CUDA_FLOAT32_BATCHED` on a paid Colab NVIDIA T4 |

Blocks are favoured over paths-per-block deliberately: uncertainty is quantified at the block level, so 64 resampling units of 3,072 paths is a better design than 32 units of 6,144 at identical cost.

**Sizing.** The narrowest bins are the two tails at roughly 2% of pairs, about 231,997 pairs each. At the observed SBJTS dispersion the row-level standard error of a tail-bin conditional mean is about 3.4e-05; inflating by the measured 1.35× block factor gives about 4.5e-05 in the tails and appreciably finer in the six interior bins — enough to resolve conditional-mean deviations of order 1e-4.

**Runtime.** Measured by timing the frozen engine at two path counts on CPU:

| probe | paths | elapsed |
|---|---|---|
| 1 | 128 | 0.56 s |
| 2 | 512 | 1.62 s |

That fits a marginal cost of about 2.76 ms per path, so the proposed budget is roughly **11 minutes** of SBJTS simulation, seconds for the Merton control, and a few minutes for the bootstrap, which works on sufficient statistics rather than raw pairs. **Request a 45-minute end-to-end allowance** on one T4 session. Peak resident memory extrapolates to about **0.9 GB**.

**Honest limitation on these figures.** They are CPU measurements. Claude has no GPU here and has not timed the CUDA path, so the T4 run may be faster or slower; the allowance is loose for that reason. A first measurement of the engine in this session came out 40× more expensive per path and was pure one-time torch warmup — which is why the reported figures come from a two-point fit after warm-up rather than a single timing.

**Why the T4 is required, scientifically.** The accepted comparator lineage ran the frozen engine under `TORCH_CUDA_FLOAT32_BATCHED`. Characterising the same law under a different numerical backend would not be the same measurement. The gate is a consistency requirement, not a performance one, and there is no CPU fallback.

## 7. Policy overlay, and what it is not

The overlay is read-only: it joins the conditional-mean curve to the already-accepted policy-response tables on the lagged-return axis, mapping the policy's raw lagged-return grid into the diagnostic's $z$ bins with the same frozen calibration used everywhere else. No policy is loaded, retrained or re-evaluated.

| constraint | arm | policy action lag slope | law conditional-mean lag slope | direction consistent |
|---|---|---|---|---|
| LONG_ONLY_FULL | SBJTS | -0.6742 | -0.1140 | `True` |
| LONG_ONLY_FULL | MERTON | +0.0145 | -0.1140 | `False` |
| LONG_ONLY_CAP50 | SBJTS | -0.2104 | -0.1140 | `True` |
| LONG_ONLY_CAP50 | MERTON | +0.0061 | -0.1140 | `False` |

DIRECTION ONLY. This overlay shows whether the sign of the learned action response to the lagged return is qualitatively consistent with the sign of the conditional structure present in the frozen target law. It does not attribute any share of the performance gap to the lagged-return channel, and it is not a test.

**Input provenance.** The two tables are inputs, not outputs of this package. They were produced by `C-RLSBJTS-MERTON-COMP-01` and are accepted research evidence; this artifact's producing ticket is the diagnostic ticket. Each is verified against its pinned digest before a row is read — `policy_response_surface.csv` `12c6f35414858552…`, `policy_response_slopes.csv` `c0ebf2b9deeda7e9…` — because a filename match is not evidence that the accepted table is the one that was read.

The direction column answers one question only: does the learned action move the way the law's own conditional mean would reward at first order, given T1's result that expected growth rises with the action when the conditional mean is positive. It is a sign comparison. It carries no magnitude, no share of the performance gap, and no test.

## 8. Claim restrictions, restated

This package does not claim, and its outputs cannot support:

- that the lagged-return coordinate causes the RL–SBJTS performance advantage;
- that a pure jump effect is isolated;
- that the conditional curve demonstrates external market validity;
- any new confirmatory hypothesis test;
- universal superiority of RL–SBJTS.

The accepted empirical claim remains the domain-scoped `CL-RL-006`. This diagnostic is post-hoc mechanism evidence supporting it, and the smoke artifacts in `evidence/conditional_law_v1/smoke/` are not scientific evidence at all.

## 9. Unresolved issues for PMO

1. **The T4 timing is unmeasured.** The budget rests on CPU timings; only the user's run will establish the CUDA cost. The 45-minute allowance is deliberately loose.
2. **Bin occupancy differs between laws by construction**, because both are binned on the Merton scale. The manuscript footnote proposed in the research README should be carried, or a reader will misread the count column.
3. **The smoke SBJTS slope is not a result.** It is computed on 384 paths to exercise the schema. I have deliberately not drawn any inference from it, and PMO should treat any quotation of it as an error.
4. **Two further descriptive quantities are implemented but unexercised at scale**: the conditional variance and the fixed-quantile tail probability by bin. They are in the output schema and the smoke fixture populates them, but their precision at the proposed budget has not been sized as carefully as the conditional mean, since the ticket names the mean curve as the primary object.

## Files

- `notebooks/07_RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1_0.ipynb` — one-pass Colab notebook; modules are carried as verified base64 so no byte differs from what was smoke-executed
- `reports/claude/RL_SBJTS_CONDITIONAL_LAW_DIAGNOSTIC_v1.md` (this file)
- `evidence/conditional_law_v1/smoke/*` — smoke artifacts and the full check record
- `evidence/conditional_law_v1/research/README_EXPECTED_OUTPUTS.md` — the expected RESEARCH schema, budget and figure specification
