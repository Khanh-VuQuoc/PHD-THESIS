# 00_CURRENT_STATE — RL–SBJTS

Updated: 2026-09-21. Owner: GPT / PMO.

## Current work

| Field | Current value |
|---|---|
| Project research status | **READY_FOR_COMPARATOR_EXTENSION** — Base 4 retained as complete estimation-first evidence with stated limitations. |
| Sole executable ticket | `tickets/C-RLSBJTS-MERTON-COMP-01.md` — **OPEN_FOR_CLAUDE**. |
| Current objective | Build and execute a fair RL–Merton/GBM comparator against the frozen RL–SBJTS target-trained policies on the same SBJTS target holdout. |
| Existing accepted evidence | Base 4: 160/160 training attempts complete, 96,000/96,000 evaluation attempts complete; target-training effect estimated under matched canonical one-step mean/variance control. |
| Existing claim status | **No RL–SBJTS > RL–Merton claim has been tested.** Base 4 compares SBJTS target training against an affine-calibrated no-jump bridge control, not against Merton/GBM. |
| Primary new comparison | SBJTS-trained policy vs Merton/GBM-trained policy, both evaluated on the frozen SBJTS target holdout. |
| Primary endpoints | `mean_terminal_log_wealth` and `cvar_log_loss`, separately for LONG_ONLY_FULL and LONG_ONLY_CAP50. |
| Secondary comparator | Analytic constrained Merton policy evaluated on the same target holdout, clearly separated from learned RL–Merton. |
| Frozen ancestry | Base 2 environment/calibration; Base 3 learner mathematics; Base 4 target law, constraints, `m=0.01`, state, wealth accounting, training budget, holdout namespaces and endpoint definitions. |
| Permanent current limitation | Base 2 ancestry is smoke-scale; no external-market-validation or universal superiority claim. |
| Next PMO decision | Audit the comparator notebook/results and decide `ACCEPTED_WITH_QUALIFICATIONS`, `TARGETED_PATCH`, or `BLOCKED`. |

## Claude start instruction

Read this state, `01_PMO_SKILL_RL_SBJTS.md`, the sole ticket, `04_CANONICAL_SOURCE_MAP.md`, and the relevant entries in `02_CLAIM_LEDGER.md` from `main` before work.

Start from the ticket's pinned baseline on an isolated branch. Preserve Base 4 exactly. Do not recalibrate SBJTS, change learner mathematics, tune on target holdout, retrofit an SESOI, or reinterpret the comparison as a pure jump effect.

The first required proof is **reproduction**: regenerate the frozen target holdout/evaluation randomness and reproduce a documented subset of Base 4 TT results before adding the Merton arm. If reproduction fails, stop and report `BLOCKED_REPRODUCTION` rather than continuing.

Commit checkpointed code/evidence. Mark only the assigned ticket `READY_FOR_PMO` when complete, then stop.

## Frozen boundaries

- SBJTS target law and frozen environment ancestry.
- Base 4 `m = 0.01` primary exploration setting.
- State `(1, t/N, log(W_t/W_0), r_{t-1})`.
- Linear actor, truncated-Gaussian action policy, linear ridge critic, Adam update mathematics.
- LONG_ONLY_FULL and LONG_ONLY_CAP50 bounds.
- 400 updates and 512 training paths/update for learned-policy comparators unless the ticket explicitly stops at smoke/preflight.
- Existing Base 4 policies/results are immutable evidence; do not overwrite them.
- Target holdout is evaluation-only.

## Closed / historical work

Base 4 remains frozen and is not reopened. Previous resolver/base3 engineering tickets are historical. The current work is an extension comparator, not a rewrite of Base 4.
