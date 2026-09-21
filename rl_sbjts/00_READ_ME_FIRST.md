# RL–SBJTS — GitHub PMO / Claude handoff

**Snapshot date:** 2026-09-21  
**Project:** Jump-Aware Exploratory Merton Portfolio Learning under Constraints (RL–SBJTS)  
**Workflow model:** adapted from the QAE Hawkes PMO workflow.

This folder is the GitHub coordination surface for the RL–SBJTS paper. It is deliberately lightweight: one authoritative state file, at most one executable Claude ticket, one compact evidence/report bundle, then one PMO decision.

## Read order

1. `00_CURRENT_STATE.md`
2. `01_PMO_SKILL_RL_SBJTS.md`
3. the sole ticket named by `00_CURRENT_STATE.md`
4. `04_CANONICAL_SOURCE_MAP.md`
5. `02_CLAIM_LEDGER.md`
6. `03_PMO_DECISION_LOG.md`

## Authority order

When GitHub is available, refresh from `main` before acting:

1. `00_CURRENT_STATE.md` — current PMO authority.
2. Sole executable ticket.
3. Latest PMO decision/handoff linked by the state.
4. `02_CLAIM_LEDGER.md`.
5. `03_PMO_DECISION_LOG.md`.
6. Frozen source/evidence identifiers in `04_CANONICAL_SOURCE_MAP.md`.
7. Older handoffs/chats — historical context only.

Do not let a notebook status string, old branch, old report, or chat summary override PMO authority on `main`.

## Current one-line state

Base 4 is retained as a **completed estimation-first study with qualifications**. The next research task is a fair, prospectively specified **RL–SBJTS versus RL–Merton/GBM comparator** on the frozen SBJTS target holdout. No RL–SBJTS > RL–Merton claim exists yet.

## Claude start instruction

> Read `rl_sbjts/00_CURRENT_STATE.md` and `rl_sbjts/01_PMO_SKILL_RL_SBJTS.md`, then execute only the unique `OPEN_FOR_CLAUDE` ticket named by the state. Work on an isolated branch. Do not alter frozen Base 4 code/results, claim status, experiment scope, or source identifiers. Commit code plus compact evidence, mark only the assigned ticket `READY_FOR_PMO`, then stop.

A posted ticket does not itself imply a PMO acceptance decision.
