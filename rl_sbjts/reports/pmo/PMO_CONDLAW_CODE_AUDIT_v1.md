# PMO conditional-law diagnostic code audit v1

**Date:** 2026-09-22  
**Submission:** `e60a3513b358064c953597a4e0e81519209239a7`  
**Ticket:** `C-RLSBJTS-CONDLAW-DIAG-01`  
**Verdict:** `TARGETED_PATCH_BEFORE_COLAB`

## Decision

The scientific design is accepted in substance, and the proposed bounded RESEARCH budget is acceptable in principle. Do **not** run the Colab RESEARCH mode yet. Two implementation/provenance issues must be patched first; neither requires new research-scale execution or a redesign of the estimand.

## What is accepted

1. **Same market object across laws.** Both arms use `project_ew(inc)`, the equally weighted log increment used by the learner and by the frozen empirical-Merton calibration.
2. **Pair construction.** `(r_{t-1}, r_t)` pairs are formed only within paths and after the lag is available; no path-boundary pairing is allowed.
3. **Common fixed bins.** The Merton-standardized right-closed bins are frozen and shared across laws. Different bin occupancy is correctly treated as a consequence of differing marginal dispersion, not as conditional-dependence evidence.
4. **Uncertainty unit.** The seed block is the resampling unit. The diagnostic does not use row-iid uncertainty as its paper inference.
5. **Controls.** The Merton iid flatness positive control, AR(1) negative control, pairing-destruction control, resume exactness, seed isolation, namespace isolation, and T4 fail-closed gate are useful and correctly targeted. The simultaneous studentized sup-statistic is preferable to requiring eight unadjusted 95% bin intervals to cover simultaneously.
6. **No retraining.** The diagnostic remains market-simulation only. The actor/critic path is excluded and the policy overlay is descriptive/read-only.
7. **Budget.** `64 blocks × 3,072 paths per law`, `4,000` block-bootstrap replicates, on the same T4/CUDA float32 market-engine lineage is bounded and scientifically adequate for this exploratory mechanism diagnostic. A 45-minute Colab allowance is acceptable even though the CUDA runtime estimate is not yet measured.
8. **Claim discipline.** `EXPLORATORY_MECHANISM_ONLY` is the correct status. No causal-share, pure-jump, external-validity, confirmatory, or universal-superiority claim is authorized.

## Blocking patch P1 — artifact provenance is wrong

Several generated smoke artifacts are stamped with the old comparator ticket rather than the conditional-law diagnostic ticket. For example:

- `evidence/conditional_law_v1/smoke/hardware_manifest.json` has `ticket = C-RLSBJTS-MERTON-COMP-01`;
- `source_fingerprint.json` has the same old ticket and comparator-specific claim wording;
- `law_summary.json` has the old ticket even though it separately carries `diagnostic_id = C-RLSBJTS-CONDLAW-DIAG-01`;
- `policy_overlay.json` is likewise stamped with the comparator ticket.

This is a provenance defect caused by reused comparator configuration. It is harmless for the smoke numbers but unacceptable before creating RESEARCH evidence.

### Required correction

All diagnostic artifacts generated in both SMOKE and RESEARCH must consistently carry, at minimum:

```text
ticket = C-RLSBJTS-CONDLAW-DIAG-01
claim_status = EXPLORATORY_MECHANISM_ONLY
```

with the correct run mode/evidence class. Remove comparator-specific wording such as “must never be reported as comparator evidence” from diagnostic manifests. If a separate `diagnostic_id` is kept, it must agree with `ticket`.

Add a cheap static/runtime gate that scans every generated JSON/CSV metadata object that carries a ticket/status field and fails if the old comparator ticket appears in diagnostic output metadata. A historical source-reference string is allowed only where explicitly labelled as provenance of an input, never as the producing ticket.

## Blocking patch P2 — remove irrelevant raw-comparator dependencies

The notebook currently stages raw Base-4/comparator artifacts such as `policies.npz`, `training_attempts.csv`, and the large `evaluation_results_partial.csv` ledger before the market-only diagnostic runs. The frozen evaluation ledger is even resolved by “largest file if ambiguous” rather than a content digest.

These files are not required to simulate the two market laws or to compute the conditional-law estimands, and the ticket explicitly asks the overlay to reuse the **already accepted compact policy-response evidence**. Leaving these dependencies in the notebook makes the Colab run more fragile and unnecessarily couples a market-law diagnostic to large raw comparator evidence.

### Required correction

- Remove unconditional staging/reading of raw policy/training/evaluation ledgers from the diagnostic path unless a file is genuinely required by an executed market-simulation function.
- For the policy overlay, use the accepted compact artifacts:
  - `evidence/merton_comparator_v1/research/policy_response_surface.csv`
  - `evidence/merton_comparator_v1/research/policy_response_slopes.csv`
  pinned by digest or carried as an embedded read-only copy with its source digest.
- If any larger artifact truly is required, document the exact executed dependency and pin it by content. Do not select a research evidence file merely by size/name ambiguity.

Add a static check that the RESEARCH diagnostic can initialize its required inputs without the raw TT evaluation ledger or policy-training ledger.

## Non-blocking notes

- The current smoke slope is not scientific evidence and must remain excluded from the manuscript.
- The research budget was sized mainly for the conditional mean, which is the ticket's primary mechanism estimand; conditional variance/tail-probability precision may be reported as secondary/exploratory if noisier.
- The policy overlay should remain a direction-only comparison against the **frozen target-law** conditional structure; it must not be interpreted as a causal decomposition of the performance gap.

## Patch acceptance criteria

Claude should patch the existing submission only, rerun the cheap unit/smoke suite, and return `READY_FOR_PMO_CODE` again. No RESEARCH mode is authorized during the patch.

PMO will authorize the user's T4 run only after:

1. all diagnostic output metadata uses the correct ticket/claim namespace;
2. irrelevant raw comparator/evaluation dependencies are removed or explicitly justified and content-pinned;
3. the cheap controls still pass;
4. the proposed RESEARCH budget and estimands remain unchanged unless PMO is told explicitly why a change is necessary.
