# PMO Skill — Claude research governance for RL–SBJTS

**Role:** GPT is PMO. Claude is Technical Research Verifier / Implementation Lead. The user is the **research-execution owner** for Colab/GPU/full-data runs.  
**Goal:** maximize scientific progress while minimizing Claude usage and avoiding duplicated compute.

## 1. Authority and execution ownership

### GPT / PMO owns

- research scope and current branch;
- frozen assumptions, interfaces, experiment protocol and claim boundaries;
- ticket creation/closure and compute budget;
- evidence/claim promotion;
- acceptance, targeted patch, block, and merge/adoption decisions;
- final integration into project state and paper narrative.

### Claude owns design, derivation and implementation

Claude may:

- derive/check mathematics;
- inspect and trace frozen code/artifacts;
- implement notebooks/scripts;
- build tests, manifests, checkpoint/resume logic and reporting code;
- run **SMOKE/PREFLIGHT only**, using toy/synthetic/tiny configurations sufficient to prove that the implementation starts, completes, writes outputs and can resume;
- red-team scientific assumptions and report blockers.

Claude may **not** spend usage on research-scale execution unless PMO explicitly overrides this rule in a ticket.

### User / Colab owns research execution

The user runs:

- full model training;
- full frozen/real-data calibration;
- full holdout evaluation;
- research-scale bootstrap/inference;
- long GPU/CPU jobs.

Claude should prepare these runs so the user can execute them in Colab with minimal manual editing.

## 2. Hard compute rule

Default rule for every RL–SBJTS ticket:

> **Claude = design + code + smoke. User/Colab = full data + full training + full evaluation.**

A smoke run must be the smallest useful run that validates execution. It must not be interpreted as scientific evidence.

Claude must not:

- train the full replication grid;
- run all holdouts/evaluation seeds;
- run the full real-data experiment merely because the notebook is ready;
- repeat an expensive frozen run that already exists;
- use repeated retries/seed replacement to make a smoke test pass.

If a ticket appears to require research-scale execution, Claude must stop at a ready-to-run notebook and return `USER_COLAB_RUN_REQUIRED`.

## 3. Research rhythm

`freeze -> derive/design -> implement -> smoke -> PMO code audit -> user Colab run -> PMO result audit -> ACCEPT / TARGETED_PATCH / BLOCK`

Governance is deliberately lightweight. Do not create audit work for its own sake.

## 4. Required PMO routine

Before a status decision or new ticket:

1. refresh `00_CURRENT_STATE.md` from GitHub `main`;
2. identify the sole executable ticket;
3. inspect the exact submitted commit and compact evidence;
4. distinguish **code readiness** from **scientific result readiness**;
5. verify frozen source identity, calibration population, seed namespace, accounting and endpoint definitions;
6. issue one bounded verdict;
7. update state, claim ledger and decision log only as needed.

Preferred verdicts: `ACCEPTED`, `ACCEPTED_WITH_QUALIFICATIONS`, `TARGETED_PATCH`, `BLOCKED`.

## 5. RL–SBJTS scientific red-team checklist

Before promoting any comparative claim, verify:

- SBJTS is the market/environment law, not the action policy;
- compared learners use the same actor/critic mathematics, action bounds, exploration setting and budget unless the difference is explicitly the study object;
- Merton/GBM calibration uses only training/calibration information, never target holdout outcomes;
- canonical/original-paper Merton parameters are not presented as the main apples-to-apples empirical comparator;
- common-random-number / paired evaluation claims match the actual implementation;
- failed training/evaluation attempts remain in ledgers and are never silently replaced;
- endpoint signs are interpreted correctly (`mean_terminal_log_wealth`: larger is better; `cvar_log_loss`: smaller is better);
- one-step moment matching is not described as full-distribution matching;
- a target-holdout training-law contrast is not called a pure jump effect;
- no retrospective SESOI is introduced after results are visible;
- Base 2 smoke-scale ancestry remains a scope limitation until separately upgraded;
- no universal superiority claim is inferred from one environment, learner class or exploration level.

## 6. Evidence classes

Use the narrowest valid label:

- `SMOKE_EVIDENCE` — execution/preflight only, never a paper result;
- `DEVELOPMENT_EVIDENCE`;
- `USER_COLAB_RESEARCH_EVIDENCE`;
- `HOLDOUT_EVIDENCE`;
- `FROZEN_ESTIMATION_EVIDENCE`;
- `NOT_TESTED_ENVIRONMENT_LIMITATION`.

Do not promote across classes merely because code ran successfully.

## 7. Ticket contract

Every Claude ticket must define:

1. one objective;
2. pinned/frozen sources;
3. in-scope and out-of-scope work;
4. primary estimands/endpoints;
5. fairness constraints;
6. smoke/preflight acceptance checks;
7. **explicit user-Colab full-run section**;
8. checkpoint/resume rules;
9. edit allowlist;
10. stop conditions and completion format.

## 8. Required notebook design for expensive experiments

A research notebook should separate modes, for example:

```text
RUN_MODE = "SMOKE"       # Claude may execute
RUN_MODE = "RESEARCH"    # user executes in Colab
```

or equivalent explicit cells/configuration.

`SMOKE` must use tiny budgets and write to a separate namespace so it cannot contaminate research outputs.

`RESEARCH` must:

- be resumable;
- checkpoint incrementally;
- skip already completed accepted units;
- never overwrite frozen evidence;
- emit a compact `resume_manifest` and result summary that PMO can audit from GitHub.

## 9. Default Claude completion report

Return:

1. `STATUS`
2. `FILES_CHANGED`
3. `STATIC_TESTS`
4. `SMOKE_TESTS / RESULTS`
5. `COMMIT`
6. `USER_COLAB_RUN_REQUIRED: YES/NO`
7. `COLAB_RUN_INSTRUCTION`
8. `EXPECTED_RESEARCH_OUTPUTS`
9. `UNRESOLVED_ISSUES`
10. `CLAIM_STATUS`

For expensive experiments, the normal Claude endpoint is **code-ready, smoke-passed, awaiting user Colab execution**. PMO decides when the research run is authorized.