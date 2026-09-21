# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-21. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **USER_COLAB_RESEARCH_AUTHORIZED** — comparator code/smoke package passed PMO code audit and is merged to `main`. |
| Sole executable ticket | `tickets/C-RLSBJTS-MERTON-COMP-01.md` — Claude implementation phase complete; user research execution now authorized. |
| Current objective | Run the direct RL–Merton/GBM comparator on the user's paid Google Colab NVIDIA T4, with U0–U3 acting as hard pre-training gates before U4–U7. |
| PMO-reviewed implementation | PR #2 / merged commit `a3d42a57718f921e2f5add9c3eead1e419cc4bc7`; source implementation commit `204f13e3f33edade7613fd9f84b2672569101e95`. |
| Existing accepted evidence | Base 4: 160/160 training attempts complete, 96,000/96,000 evaluation attempts complete; target-training effect estimated under matched canonical one-step mean/variance control. |
| Existing claim status | **No RL–SBJTS > RL–Merton claim yet.** Research evidence from the user Colab run must be audited before any promotion. |
| Primary new comparison | frozen SBJTS-trained policy vs new Merton/GBM-trained policy, both evaluated on the same frozen SBJTS target holdout. |
| Primary endpoints | `mean_terminal_log_wealth` and `cvar_log_loss`, separately for LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| Research hardware | **Paid Google Colab NVIDIA T4.** RESEARCH mode fails closed without CUDA T4. The frozen market engine runs CUDA float32 batched. |
| Learner numerical contract | The frozen Base 3 actor/critic rollout, critic fit and actor-gradient path remains vectorized NumPy float64 on CPU, exactly as in frozen Base 4. Porting this component to CUDA is a separate numerical-equivalence scope change and is **not** part of the authorized comparator run. |
| Frozen ancestry | Base 2 environment/calibration; Base 3 learner mathematics; Base 4 target law, constraints, `m=0.01`, state, wealth accounting, training budget, holdout namespaces and endpoint definitions. |
| Permanent current limitation | Base 2 ancestry is smoke-scale; no external-market-validation or universal superiority claim. |
| Next PMO decision | After the user Colab run publishes research outputs, audit source fingerprint, U1 reproduction, calibration, attempt accounting, estimands and claim status. |

## Authorized user execution

Use `rl_sbjts/notebooks/06_RL_SBJTS_VS_MERTON_COMPARATOR_GPU_v1_0.ipynb` from `main`.

Set:

```python
RUN_MODE = "RESEARCH"
ALLOW_NON_T4 = False
```

Use a paid Colab **NVIDIA T4** runtime. Run from the top with the frozen inputs under `MyDrive/sbjts_rst`.

The notebook must pass, in order:

```text
U0 source fingerprint
 -> U1 exact/tolerance-adjudicated two-holdout Base 4 reproduction
 -> U2 empirical Merton calibration
 -> U3 bounded learner positive control
 -> U4 80-policy Merton training
 -> U5 24,000 Merton target-holdout evaluations
 -> U6 analytic secondary benchmark
 -> U7 inference
```

### Hard stop rules

- If U0 fails identity/hash checks: **STOP**.
- If U1 is not `BASE4_TARGET_REPRODUCTION_PASS_EXACT` or `...PASS_WITHIN_FROZEN_BACKEND_TOLERANCE`: **STOP before U4**.
- If U1 passes only within tolerance rather than exactly, preserve the evidence and report it to PMO; this is not an automatic defect, but the backend difference must be recorded.
- If U3 reports a gross learner failure: **STOP before U4**.
- Do not alter `m`, bounds, state, budgets, seeds, holdout namespace, endpoint definitions or entropy convention during the run.
- Do not retrain frozen SBJTS policies and do not regenerate the TT arm; reuse the frozen Base 4 ledger.
- On disconnect, rerun from the top with the same `MERTONCOMP_WORK`; accepted completed units must be skipped.

## GPU interpretation

The authorized run deliberately preserves the same learner implementation used by frozen Base 4. T4 accelerates the tensor-heavy SBJTS/market simulation and block generation; the small frozen actor/critic update path remains NumPy float64 on CPU for numerical comparability. Moving that learner path to CUDA would create a new implementation lineage and requires a separate equivalence ticket before it can be used for paper evidence.

## Evidence handoff after Colab

Copy/commit the generated `evidence/merton_comparator_v1/research/` outputs to GitHub. Then return here with:

> `audit comparator Colab results`

PMO will audit the research evidence; no claim is promoted automatically.

## Closed / historical work

- Base 4 remains frozen and is not reopened.
- Commit `0bdd16b` is retained only as **DEVELOPMENT_EVIDENCE** because it executed research-scale work before the current user-Colab/T4 policy and its result files are not part of the active research tree.
- Claude's comparator implementation/smoke phase is complete; no further Claude research-scale execution is authorized for this ticket.
