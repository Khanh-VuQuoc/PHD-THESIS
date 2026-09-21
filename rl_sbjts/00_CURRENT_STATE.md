# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-21. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **COMPARATOR_IMPLEMENTATION_FOR_USER_COLAB** — Base 4 retained as complete estimation-first evidence with stated limitations. |
| Sole executable ticket | `tickets/C-RLSBJTS-MERTON-COMP-01.md` — **OPEN_FOR_CLAUDE (DESIGN + CODE + SMOKE ONLY)**. |
| Current objective | Claude prepares and smoke-validates a fair RL–Merton/GBM comparator notebook; the user runs all research-scale calibration, training, evaluation and inference in Colab. |
| Existing accepted evidence | Base 4: 160/160 training attempts complete, 96,000/96,000 evaluation attempts complete; target-training effect estimated under matched canonical one-step mean/variance control. |
| Existing claim status | **No RL–SBJTS > RL–Merton claim has been tested.** Base 4 compares SBJTS target training against an affine-calibrated no-jump bridge control, not Merton/GBM. |
| Primary new comparison | SBJTS-trained policy vs Merton/GBM-trained policy, both evaluated on the frozen SBJTS target holdout. |
| Primary endpoints | `mean_terminal_log_wealth` and `cvar_log_loss`, separately for LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| Secondary comparator | Analytic constrained Merton policy evaluated on the same target holdout, clearly separated from learned RL–Merton. |
| Execution ownership | **Claude:** derivation, code, static checks, smoke only. **User/Colab:** frozen/real-data calibration, full model training, full holdout evaluation, research-scale inference. |
| Frozen ancestry | Base 2 environment/calibration; Base 3 learner mathematics; Base 4 target law, constraints, `m=0.01`, state, wealth accounting, training budget, holdout namespaces and endpoint definitions. |
| Permanent current limitation | Base 2 ancestry is smoke-scale; no external-market-validation or universal superiority claim. |
| Next PMO decision | First audit Claude's code/smoke package. If accepted, authorize user Colab RESEARCH mode. After the user run, audit scientific results separately. |

## Claude start instruction

Read this state, `01_PMO_SKILL_RL_SBJTS.md`, the sole ticket, `04_CANONICAL_SOURCE_MAP.md`, and the relevant entries in `02_CLAIM_LEDGER.md` from `main` before work.

Claude must **not** execute the research-scale comparator. Prepare a standalone resumable notebook with a strict `SMOKE` versus `RESEARCH` split. Claude may run only the smallest smoke/preflight needed to prove the notebook, output writing and resume logic work.

Research-scale source fingerprinting against actual frozen artifacts, Base 4 reproduction, empirical Merton calibration on the real frozen training slice, positive-control run, 80-policy Merton training, 24,000 target-holdout evaluations and final inference are reserved for the user's Colab execution after PMO code audit.

Claude should mark the ticket `READY_FOR_PMO_CODE` when implementation and smoke are complete, provide exact Colab run instructions, then stop.

## Frozen boundaries

- SBJTS target law and frozen environment ancestry.
- Base 4 `m = 0.01` primary exploration setting.
- State `(1, t/N, log(W_t/W_0), r_{t-1})`.
- Linear actor, truncated-Gaussian action policy, linear ridge critic, Adam update mathematics.
- LONG_ONLY_FULL and LONG_ONLY_CAP50 bounds.
- 400 updates and 512 training paths/update for the eventual learned-policy comparator.
- Existing Base 4 policies/results are immutable evidence; do not overwrite them.
- Target holdout is evaluation-only.

## Execution policy

```text
Claude: derive -> implement -> static test -> SMOKE -> READY_FOR_PMO_CODE -> STOP
PMO: audit code/smoke -> approve or patch
User: run RESEARCH mode in Colab -> commit/publish outputs
PMO: audit research outputs -> scientific decision
```

No expensive run should be duplicated merely for verification.

## Closed / historical work

Base 4 remains frozen and is not reopened. Previous resolver/base3 engineering tickets are historical. The current work is an extension comparator, not a rewrite of Base 4.