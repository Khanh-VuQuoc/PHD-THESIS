# RL–SBJTS final claim, numerical, theory, literature and reference audit v1

**Date:** 2026-09-28  
**Manuscript audited:** `manuscript/RL_SBJTS_MANUSCRIPT_DRAFT_v1.tex` at `main` = `6ddb4a5` (includes accepted theory patch `ea86d11`).  
**Execution class:** read-only editorial audit. No experiment, training, evaluation, estimand change, evidence edit or manuscript edit was made.  
**Companion files:** `RL_SBJTS_REVIEWER_ATTACKS_v1.md`, `RL_SBJTS_FINAL_PATCH_PLAN_v1.md`.

Line numbers refer to the `.tex` file at `6ddb4a5`.

## 0. Executive summary

The accepted headline numbers, the Merton calibration, the executed-policy response values and the conditional-law values all match accepted evidence. The theory section now matches T1–T5. **Four problems matter most:**

1. **The manuscript contains no in-text citations at all** (`\cite` count = 0). The bibliography has three entries and none is cited. This is the largest gap before submission.
2. **The "moment-matched" framing is not supported by the direct comparator as reported.** The Introduction (l.27) and the Conclusion (l.179) suggest that the Merton law matches the low-order moments of the deployment law. It does not: it matches the moments of the historical training slice. Per `PMO_CONDLAW_RESULT_AUDIT_v1.md`, the SBJTS unconditional variance is `0.000262257` against Merton's `0.000172661`, about 1.52×. The unconditional means also differ: SBJTS is about `0.000373`, obtained as `E[r|bin] − deviation` from the audit table, against Merton's `0.000277`. The moment-matched evidence is Base 4, and Base 4 is not reported in the manuscript. Section 1 gives the fix.
3. **Undefined experimental primitives.** The manuscript never states:
   - the meaning of the acronym SBJTS or the SBJTS model itself;
   - the horizon `N`;
   - the CVaR level α;
   - the holdout structure (20 streams × 15 seeds, 600 paths);
   - what the "crossed-cluster" bootstrap is;
   - the common-random-number pairing.

   Several of these cannot be verified from the repository. Section 2 flags them.
4. **The mechanism section does not label the diagnostic as the lag-projected conditional law.** The quantity reported is `E_S[r_t | r_{t-1}]`, whereas T5 is stated for the full-history `μ_L(H_t)=E_L[r_t|H_t]`. The policy values are also reported without the representative state at which they were computed.

No accepted result needs to change. Every fix is wording, disclosure or citation.

---

## A. Claim–evidence audit

Classification key: **DS** directly supported · **SQ** supported with scope qualification · **TC** theory-conditional · **DO** descriptive only · **NC** needs citation · **OC** overclaim · **US** unsupported.

### A.1 Title and front matter

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| F1 | l.16 | "Training-Law Misspecification … Evidence from a Frozen SBJTS Market Law" | DEC-RL-004 scope | SQ | Yes | — |
| F2 | l.17 | "Manuscript core assembled from the locked RL--SBJTS research record" | — | — | No (placeholder) | Real author block (P3). |

### A.2 Abstract (l.23)

| # | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|
| AB1 | "deployment returns exhibit jump-rich and temporally dependent structure" | Temporal dependence: condlaw audit, lag slope −0.125. Jumps exist by construction (theory report §T5, source inspection). No jump-frequency statistic is reported anywhere. | OC (mild) | No | "when the deployment law contains jump and temporal-dependence components". |
| AB2 | "holds the learner, state representation, exploration parameter, optimization budget, portfolio constraints, and deployment environment fixed, while changing only the training law" | DEC-RL-003/004 design; canonical source map §D | DS | Yes | — |
| AB3 | "a frozen SBJTS path generator versus an empirically calibrated iid Merton/GBM diffusion" | Calibration in `RL_SBJTS_PAPER_SCIENTIFIC_UPDATE_v1.md` §3.2 | DS | Yes | Add "calibrated to the same historical training slice" so readers do not assume the Merton law is calibrated to the SBJTS law. |
| AB4 | "SBJTS-trained policies achieve higher mean terminal log wealth and lower CVaR log loss under both …" | `RESEARCH_RESULT_SNAPSHOT.json` | SQ | Yes (scoped by "On the same frozen SBJTS deployment law") | "achieve **estimated** higher …" (optional). |
| AB5 | "Δ_W=0.0022063 … Δ_CVaR=−0.0031810 … 0.0005541 and −0.0007611" | Snapshot deltas 0.00220632 / −0.00318095 / 0.00055409 / −0.00076106 | DS | Yes | Use one rounding convention across abstract and table (P3). |
| AB6 | "Crossed-cluster intervals and a policy-level sensitivity analysis … preserve all four directions" | Snapshot: crossed and policy-level CIs | DS | Yes, but vague | "exclude zero for all four contrasts". |
| AB7 | "The difference is not explained by average risky exposure." | Mean exposure 0.500677 vs 0.499760 (FULL), 0.249915 vs 0.249670 (CAP50) | OC (mild) | No | "The difference is not accompanied by a material difference in average executed risky exposure." Near-equal means show that the gain is not a level effect. They do not exclude every exposure-related explanation, such as dispersion or timing. |
| AB8 | "A theory layer shows that local moment matching does not imply RL equivalence" | T2 (existence, constructive) | TC | Yes if read as existence | "shows that matching local moments **need not** imply RL equivalence". |
| AB9 | "… and decomposes market-law effects through exact wealth coupling, state occupancy, continuation values, and conditional information" | T1, T4, T5 | OC (mild) | No | T4 decomposes the **policy-gradient gap**, not "market-law effects" on performance, and only as an attribution convention. Suggested: "and organizes how the training law enters the problem: exact wealth coupling, and a gradient-gap identity with occupancy, continuation-value and entropy terms (an attribution convention, not a causal decomposition)". |
| AB10 | "A final user-run diagnostic on 196,608 paths per law" | Condlaw audit | DS | Yes, but "user-run" is internal jargon | "A simulation diagnostic on 196,608 paths per law". |
| AB11 | "the frozen SBJTS return has pronounced negative lag dependence and state-dependent conditional variance and tail risk" | Condlaw audit §§3–4 | DO | Yes | Add "lag-conditional" to make the lag projection explicit (see A.8). |
| AB12 | "iid Merton control is recovered as flat" | Condlaw audit §2 | DS | Yes | — |
| AB13 | "Saved SBJTS policies adjust risky exposure in a direction qualitatively aligned with this conditional structure, whereas Merton-trained policies are nearly insensitive to lagged return" | Mechanism note §4; `policy_response_surface.csv` | DO | Yes | — |
| AB14 | "The evidence is domain-scoped and descriptive rather than a universal or single-channel causal claim." | All PMO notes | DS | Yes | — |

### A.3 Introduction (l.27–31)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| I1 | l.27 | "Continuous-time portfolio models often compress the risky-return law into a small number of diffusion parameters." | Merton 1969/1971 | NC | Yes, after citing | Cite Merton 1969, 1971. |
| I2 | l.27 | "does a training law that matches local return moments but omits path dependence define the same reinforcement-learning problem?" | T2 answers the general question. The direct comparator does **not** match the deployment law's moments (variance ratio ≈1.52, means differ; condlaw audit §§2–4). | OC by implication | No | Keep the question but decouple it from the experiment. Say (i) T2 answers it in general, (ii) Base 4 addresses it empirically with a moment-matched control (if reported), and (iii) the direct comparator is a **data-calibrated** Merton law, not a moment-matched one. Suggested sentence after l.27: "The direct comparator below calibrates the Merton law to the same historical training slice rather than to the moments of the simulated deployment law, so it measures the cost of the standard diffusion calibration, not of a moment-matched diffusion." |
| I3 | l.29 | "frozen SBJTS path generator calibrated from historical multi-asset returns and designed to preserve jump/path/temporal structure" | Research update §3.2 (ITA, XLE, SMH, EUFN; 2012-01-04 to 2020-05-22; 2,110 obs.); source inspection §T5 | SQ + NC | Partly | The acronym is never expanded and the model is never specified or cited. Add the expansion, a reference to the SBJTS source paper or technical record, and the fact that its calibration ancestry is smoke-scale (DEC-RL-001). The expansion is **not** in the repository; the author must supply it. |
| I4 | l.29 | "The second is an empirical Merton/GBM comparator calibrated from the same frozen training slice to the mean and variance of the equally weighted risky log increment." | Research update §3.2 | DS | Yes | — |
| I5 | l.31 | Non-claims paragraph | DEC-RL-004 | DS | Yes | Add "that the results transfer to historical markets" and "that this is a confirmatory test", which are the two permanent limitations currently missing here. |
| I6 | — | *Missing:* any statement of contribution or positioning relative to Chau–Nguyen–Nguyen, the exploratory-control literature, jump-diffusion RL or risk-sensitive RL | — | — | — | See section E and patch P2-1. |

### A.4 Baseline and frozen objective (l.33–44)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| B1 | l.36–38 | State `S_t=(1,t/N,log(W_t/W_0),r_{t-1})` … "not asserted to be a complete Markov state" | Canonical map §D; theory §T3 | DS | Yes | — |
| B2 | l.38 | "actor is linear in S_t before a bounded transformation maps its outputs to the location and scale of a truncated Gaussian" | Theory §T3.0 | DS | Yes | — |
| B3 | l.38 | Constraints `[0,1]`, `[0,0.5]` | Canonical map §D | DS | Yes | — |
| B4 | l.42 | `J_disc(θ)=E_θ[log(W_T/W_0)] + m Σ_t H(λ_θ(·|S_t))` | The theory report and l.102 put the entropy sum **inside** the expectation | **Math error (notation)** | No | `J_disc(θ)=E_θ[ log(W_T/W_0) + m Σ_{t=0}^{N-1} H(λ_θ(·|S_t)) ]`. |
| B5 | l.44 | "m=0.01 and Δt=1/250. If continuous-time notation uses λ∫H dt, then m=λΔt." | Theory report "Entropy time-scaling"; research update §7 | DS but incomplete | Partly | Add: "The frozen m=0.01 therefore corresponds to a continuous-time temperature of 2.5, not 0.01; a continuous-time temperature of 0.01 would correspond to m=4×10⁻⁵." Also rename the temperature (e.g. γ), because λ already denotes the policy density λ_θ. |
| B6 | — | *Missing:* horizon N, CVaR level α, definition of "CVaR log loss", learner details (critic, Adam, 400 updates × 512 paths) | Canonical map §D gives updates and paths. N=60 appears only in the condlaw environment fingerprint. α is **not in the repository**. | US (by omission) | — | State all of them; α must come from the frozen protocol (flagged in B.3). |

### A.5 Market laws and experimental design (l.46–53)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| D1 | l.47 | "The frozen SBJTS target law produces the equally weighted projected risky log increment consumed by the learner." | Research update §3.1 | DS | Yes | Give a model description (appendix) or a citation. |
| D2 | l.49–51 | Calibration formulas and values | Recomputed: σ_M=0.2077734, μ_M−r_f=0.0914416 | DS | Yes | State the `ddof` convention (canonical map §C requires it; not visible in the repository). |
| D3 | l.51 | "Merton increments are iid Gaussian by construction." | Theory report §T5 | DS | Yes | — |
| D4 | l.53 | "same learner, optimizer, state representation, exploration parameter, constraints, number of updates, paths per update, and deployment law" | DEC-RL-003 | DS | Yes | — |
| D5 | l.53 | "Forty training replications per constraint for each training law … Merton arm contributes 80 trained policies and 24,000 target-holdout evaluations" | Snapshot: 80/80 trained, 24,000/24,000 evaluated | DS | Yes | Add the holdout structure: 20 holdout streams × 15 seeds = 300 blocks per policy, 600 paths per evaluation; common random numbers across arms. |
| D6 | l.53 | "Frozen SBJTS evaluation rows are reused" | DEC-RL-004 (reuse; bitwise-exact two-holdout reproduction on 16 rows) | DS | Internal jargon | "The SBJTS arm's evaluations are those of the previously frozen study; a reproduction check on 16 predeclared rows matched bitwise." Disclose the single duplicate row removed in pairing (DEC-RL-004). |
| D7 | — | *Missing:* the SBJTS arm is trained **on the deployment law itself**, with disjoint seeds | Design | — | — | Must be stated. It defines what the comparison measures (see reviewer attack R1). |

### A.6 Theory (l.55–142)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| T1a | l.57–62 | Exact wealth coupling | Theory §T1 | DS | Yes | — |
| T1b | l.64–68 | Taylor expansion "Locally around r=0 … used only as a local diagnostic" | Theory §T1.2–1.3 | DS | Yes | — |
| T2a | l.70–72 | Proposition (existence; also with identical one-step marginals) | Theory §T2a/T2b | TC (constructive) | Yes | Add a proof sketch or appendix pointer. Phrase the gradient part as the derivative statement (T2b caveat: the argmax lies on a grid boundary). |
| T3a | l.74–115 | A1–A4, two scores, two-term gradient, A4-mixed assumed, not proved, withdrawn reduction noted | PMO theory-patch audit §2 | TC | Yes | Ordering: ψ_θ and R^soft are used in (A4) before they are defined (P3). |
| T4a | l.117–134 | Common dominating measure, symmetric midpoint identity, three pieces, "attribution convention, not a causal decomposition" | PMO theory-patch audit §3 | TC | Yes | Add one sentence saying the identity is **not estimated** on the frozen problem and is verified only on an enumerable fixture. |
| T5a | l.137–141 | Covariance identity; "Under iid Merton, μ_M(H_t) is constant and the covariance channel vanishes" | Theory §T5 | DS (theory) | Yes | — |
| T5b | l.142 | "This establishes the availability of a lag-dependent information channel under a history-dependent law, and its absence under the iid law." | PMO theory-patch audit §4 (do not broaden to "every lag-related effect") | Slightly broad | Borderline | "…and the vanishing of this conditional-mean covariance term under the iid law." ("its absence" could be read as ruling out every lag-related policy effect.) |

### A.7 Main results (l.144–166)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| R1 | Table, l.148–163 | All primary values | See B.1 | DS (one flagged digit) | Yes | Report CIs to at most 3–4 significant figures (B.1 digit conflict). |
| R2 | l.166 | "All four crossed-cluster intervals exclude zero in the direction favoring SBJTS training." | Snapshot | DS | Yes | Define the crossed-cluster bootstrap (training-replication × holdout-block clusters) in design. Avoid the word "significant". |
| R3 | l.166 | "A policy-level sensitivity … excludes zero for all four contrasts, with the favorable sign in 40/40 replications" | `policy_level_sensitivity.csv` | DS | Yes | Optionally give the policy-level CIs (B.1). |
| R4 | — | *Missing:* economic scale. Δ_W is about 22 bp of horizon log wealth, ≈17.5% of the Merton arm's mean terminal log wealth (0.0022063/0.0126367); Δ_CVaR is ≈3.7% of Merton CVaR (0.0031810/0.0870395) | Research update §4.1 (bp statement) | DS (arithmetic) | — | Add one sentence: horizon-level, not annualized. |
| R5 | — | *Missing:* CAP50 attenuation (≈25% of FULL for wealth, ≈24% for CVaR) | Research update §4.2 | DS | — | Optional sentence. Keep the research note's interpretation ("largest when the policy has enough action freedom") as a hypothesis, not a finding. |

### A.8 Mechanism evidence (l.168–173)

| # | Location | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|---|
| M1 | l.169 | "64 seed blocks of 3,072 paths per law … 196,608 paths and 11,599,872 lagged-return pairs … 4,000 block-bootstrap replications" | Condlaw audit §1 | DS | Yes | — |
| M2 | l.169 | "iid Merton control has lag slope +0.0001347 with 95% CI [−0.0004298,+0.0007155]" | Condlaw audit §2 | DS | Yes | — |
| M3 | l.169 | "SBJTS has lag slope −0.125006 … and lag-1 autocorrelation −0.124750" | Condlaw audit §3 | DO | Yes, but unlabeled | Name the estimand: "the least-squares slope of r_t on r_{t−1}, i.e. a summary of the lag-projected conditional mean E_S[r_t|r_{t−1}], which coarsens the full-history μ_S(H_t) used in the theory". This distinguishes the lag-projected law from the full-history law. |
| M4 | l.171 | Conditional-variance values 0.0002623 / 0.0009073 / 0.0004576 | Condlaw audit §4 | DO | Yes | Define the lag bins (they are labeled `(−inf,−2]` … `(2,inf)`; the audit's mean lagged return in the extreme bins, −0.0534 and +0.0557, implies standardized units, but the standardization is **not stated in the repository**. Flag in B.3.) |
| M5 | l.171 | "SBJTS left-tail probability rises to 7.85% in the most positive lag bin, while Merton remains near 5% across bins" | Condlaw audit §4 | DO | Yes | Optionally add the exact extreme-negative bin value 3.19%. Keep the state file's "2.8–3.2%" only if marked rounded (PMO instruction). Do not interpret causally. |
| M6 | l.173 | "SBJTS-trained mean risky allocation moves from about 0.543 at lag −0.06 to 0.462 at lag +0.06, while the Merton-trained policy remains near 0.495–0.496" | `policy_response_surface.csv`: 0.542746 → 0.461685; Merton 0.494688–0.496431 | DO | Missing qualifier | Add "at the representative state t/N=0.5, log(W_t/W_0)=0, averaged over the 40 saved policies". Note that ±0.06 is roughly 3.7 SBJTS unconditional standard deviations (√0.000262≈0.0162), i.e. tail states. |
| M7 | l.173 | "Saved policies align qualitatively with this structure." | Condlaw audit §5 | DO | Yes | — |
| M8 | — | Executed-policy slopes (−0.674 / +0.015) not quoted; raw coefficients (−1.56) not quoted | Supersession note §E | — | Safe now | If slopes are added, label them "local derivative of the executed mean action at the representative state"; never quote −1.56 as a slope. |

### A.9 Discussion and limitations (l.176)

| # | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|
| L1 | "changing the trajectory law while holding the learner and deployment environment fixed changes the learned feedback rule and deployment outcomes" | Controlled simulation design (training law is the manipulated factor) | SQ | Yes within design | Add "in the tested setting". The manipulated factor bundles every difference between the two laws: jumps, dependence **and** unconditional mean/variance. |
| L2 | "does not identify a pure-jump effect or a causal share attributable to one state coordinate" | DEC-RL-004 | DS | Yes | — |
| L3 | "deployment environment is simulated, one exploration level is primary, the observation is partial, and the policy-gradient theorem remains conditional" | DEC-RL-004, theory acceptance | DS | Yes | **Missing limitations**, each a permanent PMO restriction: (a) SBJTS calibration ancestry is smoke-scale, so no external-market validity; (b) estimation-first, with no prespecified SESOI or confirmatory test; (c) the Merton arm is data-calibrated and not moment-matched to the deployment law; (d) a single linear-actor, truncated-Gaussian learner, with no claim of policy-class optimality; (e) T4 is not estimated on the frozen problem. |

### A.10 Conclusion (l.179)

| # | Current wording | Evidence | Class | Safe? | Minimal correction |
|---|---|---|---|---|---|
| C1 | "the frozen SBJTS training law produces higher terminal log wealth and lower CVaR log loss on the tested SBJTS deployment environment under both portfolio constraints" | Snapshot | SQ | Yes | — |
| C2 | "The average risky exposure is nearly unchanged, but the learned feedback rule differs." | Snapshot, surface | DS | Yes | — |
| C3 | "…training-law misspecification can matter … **even when local low-order return moments are matched**" | T2 is existence-only. The direct comparator is **not** moment-matched to the deployment law. Base 4 is not reported. | **OC** | **No** | Either (i) "…can matter to constrained exploratory portfolio reinforcement learning; the theory shows that matching local low-order moments is not sufficient in general", or (ii) keep the phrase only if a Base 4 paragraph is added (PMO decision, P0-2). |

---

## B. Numerical consistency audit

Sources: `evidence/merton_comparator_v1/research/RESEARCH_RESULT_SNAPSHOT.json` (SN), `policy_level_sensitivity.csv` (PL), `policy_response_surface.csv` (PS), `policy_response_slopes.csv` (SL), `PMO_CONDLAW_RESULT_AUDIT_v1.md` (CA), `PMO_MANUSCRIPT_INTEGRATION_v1.md` (MI), `RL_SBJTS_MECHANISM_AND_ROBUSTNESS_v1.md` (MR).

### B.1 Direct comparator

| Quantity | Manuscript | Accepted evidence | Status |
|---|---|---|---|
| FULL TT mean terminal log wealth | 0.0148430 | SN 0.01484303 | ✔ |
| FULL MT mean terminal log wealth | 0.0126367 | SN 0.01263671 | ✔ |
| FULL Δ_W | 0.00220632 (table), 0.0022063 (abstract) | SN 0.0022063172 | ✔ (two roundings) |
| FULL Δ_W CI | [0.00217262, 0.00224227] | SN [0.0021726218, 0.0022422710] | ✔ |
| FULL TT CVaR | 0.0838585 | SN 0.08385853 | ✔ |
| FULL MT CVaR | 0.0870395 | SN 0.08703948 | ✔ |
| FULL Δ_CVaR | −0.00318095 / −0.0031810 | SN −0.0031809539 | ✔ |
| FULL Δ_CVaR CI | [−0.00336362, −0.00299560] | SN [−0.0033636218, −0.0029956024] | ✔ |
| CAP50 TT mean terminal log wealth | 0.00752284 | SN 0.007522836 | ✔ |
| CAP50 MT mean terminal log wealth | 0.00696874 | SN 0.006968744 | ✔ |
| CAP50 Δ_W | 0.000554092 / 0.0005541 | SN 0.0005540917 | ✔ |
| CAP50 Δ_W CI low | **0.000545001** | SN **0.000544995** (stored at 9 dp); MI 0.000545001; research update 0.00054500 | **⚠ CONFLICT at the 9th decimal.** Both round to 0.000545 (6 dp). The repository snapshot stores CAP50 bounds at reduced precision, so the manuscript's extra digits cannot be verified. **Do not guess.** Recommend reporting all CIs to 4 significant figures (0.0005450), or PMO confirms from `primary_estimands.json` on Drive. |
| CAP50 Δ_W CI high | 0.000563736 | SN 0.00056374 (8 dp) | ✔ at stored precision; the extra digit is unverifiable in the repository |
| CAP50 TT CVaR | 0.0415466 | SN 0.041546635 | ✔ |
| CAP50 MT CVaR | 0.0423077 | SN 0.042307699 | ✔ |
| CAP50 Δ_CVaR | −0.000761064 / −0.0007611 | SN −0.0007610644 | ✔ |
| CAP50 Δ_CVaR CI | [−0.000810332, −0.000712501] | SN [−0.00081033, −0.00071250] | ✔ at stored precision; extra digits unverifiable in the repository |
| Policy-level CIs (not in manuscript) | "excludes zero" | PL / SN: FULL W [0.0021809, 0.0022334]; FULL CVaR [−0.0032174, −0.0031439]; CAP50 W [0.0005474, 0.0005611]; CAP50 CVaR [−0.0007693, −0.0007524] | ✔ |
| 40/40 favorable | 40/40 | PL `favorable_count=40`, `n_policy=40` | ✔ |
| Mean exposure FULL | 0.500677 / 0.499760 | SN | ✔ |
| Mean exposure CAP50 | 0.249915 / 0.249670 | SN | ✔ |
| Merton trained / evaluated | 80 / 24,000 | SN 80/0 failed/0 replacements; 24,000/0 | ✔ |

### B.2 Calibration, entropy, sample sizes

| Quantity | Manuscript | Check | Status |
|---|---|---|---|
| m₁ | 2.7942696×10⁻⁴ | Research update §3.2 | ✔ |
| v₁ | 1.7267919×10⁻⁴ | Research update §3.2 | ✔ |
| σ_M = √(v₁/Δt) | 0.2077734 | recomputed 0.20777343 | ✔ |
| μ_M−r_f = m₁/Δt + ½σ_M² | 0.0914416 | recomputed 0.09144164 | ✔ |
| m, Δt | 0.01, 1/250 | canonical map §D | ✔ |
| m=λΔt ⇒ λ_equiv | not stated | 0.01/(1/250) = 2.5; λ=0.01 ⇒ m=4×10⁻⁵ | Add (A.4 B5) |
| Condlaw budget | 64 × 3,072 = 196,608; 11,599,872 pairs; 4,000 bootstrap | CA §1; 196,608 × 59 = 11,599,872 ✔ (so N=60 steps per path is consistent) | ✔ |

### B.3 Mechanism numbers

| Quantity | Manuscript | Accepted evidence | Status |
|---|---|---|---|
| Merton lag slope, CI | +0.0001347, [−0.0004298, +0.0007155] | CA §2 | ✔ |
| SBJTS lag slope, CI | −0.125006, [−0.125843, −0.124150] | CA §3 | ✔ |
| SBJTS lag-1 autocorrelation | −0.124750 | CA §3 | ✔ (CI [−0.125587, −0.123909] available, not quoted) |
| SBJTS unconditional variance | 0.0002623 | CA 0.000262257 | ✔ |
| Most-negative-bin variance | 0.0009073 | CA 0.000907299 | ✔ |
| Most-positive-bin variance | 0.0004576 | CA 0.000457573 | ✔ |
| Most-positive-bin tail probability | 7.85% | CA 7.85% | ✔ |
| Merton tail ≈5% in every bin | "near 5%" | CA §2 | ✔ |
| Policy FULL SBJTS 0.543 → 0.462 | 0.543 / 0.462 | PS 0.542746 / 0.461685 | ✔ (representative-state qualifier missing) |
| Policy FULL Merton 0.495–0.496 | 0.495–0.496 | PS 0.494688–0.496431 | ✔ at 3 dp |
| Executed slopes (if added) | — | SL FULL lag SBJTS −0.6742 / Merton +0.0145; CAP50 −0.2104 / +0.0061 | Must be labeled as executed-policy local slopes, not raw coefficients |

**Unverifiable from the repository, flagged:**

1. **CVaR level α** for `cvar_log_loss`: not in any repository file. Needed for the paper.
2. **Horizon N** for the comparator: `N_STEPS=60`, `dt=0.004` appear only in the condlaw environment fingerprint, which is stated to match the frozen lineage. The pair count (59 per path) is consistent. PMO should confirm this is the comparator horizon.
3. **Lag-bin standardization** (units of the `(−inf,−2]` … `(2,inf)` bins).
4. **Conditional-law research tables**: the repository holds only `research/README_EXPECTED_OUTPUTS.md`. The values are verified against the PMO audit, which cites Drive file IDs but, unlike the comparator's `ARTIFACT_MANIFEST.json`, gives **no SHA-256 pins**. This is a provenance asymmetry, not an error.
5. **The "2.8–3.2%" range** in `00_CURRENT_STATE.md`: PMO reports it verified against the raw table. It is not reproducible from repository files. The manuscript does not use it.

No smoke-evidence number appears in the manuscript. The only smoke tail table in the repository, `smoke/tail_probability_bins.csv` (e.g. Merton extreme bin 6.28%), is not quoted.

---

## C. Theory-to-manuscript consistency

| Item | Requirement | Manuscript | Status |
|---|---|---|---|
| T1 | Exact coupling primary; Taylor local only | l.57–68 | ✔ |
| T2 | Existence only; no stronger claim | l.70–72 ("There exist…") | ✔ (add proof pointer). ⚠ Conclusion l.179 and Intro l.27 lean on it more strongly than its existence form supports (A.10 C3). |
| T3 | A1–A4 | l.82–88 | ✔ |
| T3 | Policy-parameter vs actor-weight score | l.95–99 | ✔ |
| T3 | Direct entropy derivative separate | l.105–109 | ✔ |
| T3 | A4-mixed assumed sufficient, not proved | l.111–115 | ✔ |
| T3 | Withdrawn first-moment reduction does not reappear as a claim | l.115 mentions it only as withdrawn | ✔ |
| T3 | S_t not Markov | l.38, l.75, l.93 | ✔ |
| T4 | Common dominating measure ν | l.118–121 | ✔ |
| T4 | Symmetric midpoint convention | l.126–128 | ✔ |
| T4 | Entropy occupancy-difference term | l.130–134 | ✔ |
| T4 | Not causal | l.134 | ✔ |
| T5 | Availability, not attribution | l.142 | ✔ (narrow "its absence", A.6 T5b) |
| Entropy | m = λΔt | l.44 | ✔, but λ is overloaded (policy density vs temperature) and λ_equiv=2.5 is not stated. m=0.01 is nowhere equated with a continuous-time 0.01 ✔. |
| Objective | Entropy inside expectation | l.42 ✘ vs l.102 ✔ | Fix l.42 |
| Lag projection | Diagnostic measures E[r_t|r_{t−1}], theory uses μ(H_t) | l.169 unlabeled | Label (A.8 M3) |

---

## D. Literature audit

"Verified" means confirmed by web search on 2026-09-28 (sources in section G). "UNVERIFIED" entries must not be added until confirmed. None of these references is added to the manuscript in this pass.

### D.1 Continuous-time portfolio RL and exploratory control

- **Currently covered:** Chau–Nguyen–Nguyen, listed but not cited.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| H. Wang, T. Zariphopoulou, X. Y. Zhou (2020), "Reinforcement learning in continuous time and space: A stochastic control approach," *JMLR* 21(198). Verified; page range to confirm. | Origin of the entropy-regularized exploratory formulation behind the λ∫H dt objective and the m=λΔt statement. | ESSENTIAL |
| H. Wang, X. Y. Zhou (2020), "Continuous-time mean–variance portfolio selection: A reinforcement learning framework," *Mathematical Finance* 30(4):1273–1308, doi 10.1111/mafi.12281. Verified. | First exploratory portfolio RL; Gaussian exploration. | HIGH VALUE |
| Y. Jia, X. Y. Zhou (2022), "Policy gradient and actor–critic learning in continuous time and space: Theory and algorithms," *JMLR* 23(275):1–50. Verified. | Continuous-time policy-gradient counterpart; positions the discrete T3. | HIGH VALUE |
| X. Gao, L. Li, X. Y. Zhou, "Reinforcement learning for jump-diffusions, with financial applications," arXiv:2405.16449. Verified as arXiv; journal status UNVERIFIED. | **Directly relevant:** exploratory RL under jump-diffusion dynamics. It notes that jumps should affect actor/critic parameterization. The closest existing link between "jumps" and "exploratory RL". | ESSENTIAL |
| T. Nguyen, P. Nkuize (2026), "Optimal investment and entropy-regularized learning under stochastic volatility models with portfolio constraints," arXiv:2604.22188. Verified as arXiv. | Closest competitor: constrained exploratory investment beyond GBM with a truncated-Gaussian optimum. Must be distinguished (they treat a Markov factor model analytically; this paper studies training-law misspecification with a history-dependent simulator). | ESSENTIAL (positioning) |
| M. Dai, Y. Dong, Y. Jia, X. Y. Zhou, "Learning Merton's strategies in an incomplete market: recursive entropy regularization and biased Gaussian exploration," arXiv:2312.11797. Verified as arXiv; venue UNVERIFIED. | Exploratory Merton beyond complete GBM markets. | OPTIONAL |
| C. Bender, N. T. Thuan, "Entropy-regularized mean-variance portfolio optimization with jumps," arXiv:2312.13409. Verified as arXiv. | Exploratory portfolio with Lévy jumps. | OPTIONAL |

### D.2 Classical Merton theory

- **Currently covered:** Merton 1969 and 1971, listed but not cited.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| J. Cvitanić, I. Karatzas (1992), "Convex duality in constrained portfolio optimization," *Ann. Appl. Probab.* 2(4):767–818. Verified; doi 10.1214/aoap/1177005576 per Project Euclid URL. | Classical constrained-portfolio benchmark for the long-only and 50%-cap constraints. | HIGH VALUE |

### D.3 Jump / self-exciting / path-dependent return models

- **Currently covered:** none.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| **The SBJTS model's own source** (paper or technical record). Not in the repository; the author must supply it. | Defines the simulator. Without it the paper is not reproducible or reviewable. | **ESSENTIAL** |
| R. C. Merton (1976), "Option pricing when underlying stock returns are discontinuous," *JFE* 3(1–2):125–144. Verified. | Canonical jump-diffusion. Positions "jump-rich" versus the Merton diffusion. | ESSENTIAL |
| A. G. Hawkes (1971), "Spectra of some self-exciting and mutually exciting point processes," *Biometrika* 58(1):83–90. Verified. | Self-exciting intensity. Include **only if** the SBJTS jump intensity is self-exciting; the theory report §T5 says it is built from accumulated path kernel weights, so the author should confirm. | HIGH VALUE (conditional) |
| Y. Aït-Sahalia, J. Cacho-Diaz, R. J. A. Laeven (2015), "Modeling financial contagion using mutually exciting jump processes," *JFE* 117(3):585–606. Verified. | Hawkes jumps in asset returns; the finance anchor for path-dependent jump intensity. | HIGH VALUE (conditional, as above) |

### D.4 RL under model misspecification / simulator mismatch

- **Currently covered:** none.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| A. Nilim, L. El Ghaoui (2005), "Robust control of Markov decision processes with uncertain transition matrices," *Oper. Res.* 53(5):780–798. Verified. | Transition-law misspecification in MDPs. Contrast: robust MDPs hedge over an ambiguity set, whereas this paper measures the cost of one specific misspecified training law. | HIGH VALUE |
| G. N. Iyengar (2005), "Robust dynamic programming," *Math. Oper. Res.* 30(2):257–280, doi 10.1287/moor.1040.0129. Verified. | Same role. | HIGH VALUE (cite one or both) |
| W. Zhao, J. P. Queralta, T. Westerlund (2020), "Sim-to-real transfer in deep reinforcement learning for robotics: a survey," IEEE SSCI, 737–744. Verified. | Simulator-to-deployment mismatch as a general RL problem. | OPTIONAL |

### D.5 Risk-sensitive and constrained portfolio RL

- **Currently covered:** none.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| R. T. Rockafellar, S. Uryasev (2000), "Optimization of conditional value-at-risk," *J. Risk* 2(3):21–41. Verified. | Definition of CVaR used for the co-primary endpoint. | ESSENTIAL |
| A. Tamar, Y. Glassner, S. Mannor (2015), "Optimizing the CVaR via sampling," *AAAI* 29(1). Verified. | Positioning: this paper **evaluates** CVaR and does not optimize it. | HIGH VALUE |
| Y. Chow, A. Tamar, S. Mannor, M. Pavone (2015), "Risk-sensitive and robust decision-making: a CVaR optimization approach," *NeurIPS* 28, 1522–1530. Verified. | Links CVaR to robustness against model error. | OPTIONAL |
| B. Hambly, R. Xu, H. Yang (2023), "Recent advances in reinforcement learning in finance," *Mathematical Finance* 33(3):437–503, doi 10.1111/mafi.12382. Verified. | One survey anchor for portfolio RL, instead of a long generic list. | HIGH VALUE |

### D.6 Policy-gradient theory under history dependence / partial observation

- **Currently covered:** none. T3 is presented without precedent.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| R. J. Williams (1992), "Simple statistical gradient-following algorithms for connectionist reinforcement learning," *Machine Learning* 8:229–256, doi 10.1007/BF00992696. Verified. | The likelihood-ratio (REINFORCE) identity that T3 specializes. | ESSENTIAL |
| J. Baxter, P. L. Bartlett (2001), "Infinite-horizon policy-gradient estimation," *JAIR* 15:319–350. Verified. | Policy gradients for **partially observable** processes with observation-based stochastic policies. T3's "no Markov assumption on S_t" must be credited to this line of work. | ESSENTIAL |
| Sutton, McAllester, Singh, Mansour (2000), policy-gradient theorem with function approximation, NeurIPS 12. **UNVERIFIED in this pass.** | Occupancy-measure form of the gradient used in T4. | HIGH VALUE; verify before adding |

### D.7 Moment matching vs path-law equivalence

- **Currently covered:** none.
- **Missing:**

| Reference | Role | Priority |
|---|---|---|
| A. W. Lo, A. C. MacKinlay (1988), "Stock market prices do not follow random walks: evidence from a simple specification test," *RFS* 1(1):41–66. Verified. | Multi-period variance depends on autocovariances (variance-ratio logic). This is exactly Base 4's diagonal versus cross-time decomposition. | HIGH VALUE if Base 4 is reported, else OPTIONAL |

**Suggested bibliography size:** 3 existing + about 12 load-bearing references (the ESSENTIAL and HIGH VALUE items above), about 15 in total.

---

## E. Novelty positioning

### E.1 Methodological / theoretical

- **What existed before:**
  - exploratory entropy-regularized control and its portfolio application (Wang–Zariphopoulou–Zhou; Wang–Zhou);
  - the constrained truncated-Gaussian optimum under GBM (Chau–Nguyen–Nguyen), since extended to stochastic volatility (Nguyen–Nkuize);
  - exploratory RL under jump-diffusions (Gao–Li–Zhou);
  - likelihood-ratio policy gradients for partially observed, observation-based policies (Williams; Baxter–Bartlett).
- **What this paper adds:**
  - (i) a constructive result that matching unconditional one-step mean/variance, or even the full one-step marginal, need not yield the same growth functional, optimum or gradient, stated for the frozen constrained learner;
  - (ii) the specialization of the trajectory gradient to this learner with an explicit separation of the policy-parameter score from the actor-weight score, and the resulting mixed state/soft-return domination condition;
  - (iii) a symmetric occupancy / continuation-value / entropy-occupancy identity for the **training-law gradient gap** under a common dominating measure;
  - (iv) the covariance "availability" result for lag information.
- **What it does NOT add:**
  - a new RL algorithm;
  - a new policy-gradient theorem in general form;
  - convergence or optimality results;
  - verification of A4 for SBJTS;
  - an estimate of the T4 channels on the real problem.

### E.2 Empirical

- **What existed before:** analytic and learned exploratory policies are studied mostly within the model they are derived for, whether GBM, factor or jump-diffusion.
- **What this paper adds:** a controlled, replicated (40 paired replications per constraint), pre-frozen comparison of the *same* constrained learner trained under a data-calibrated GBM versus a history-dependent jump simulator, evaluated on the same simulated deployment law. It reports estimated wealth and CVaR effects with two levels of clustering.
- **What it does NOT add:**
  - evidence on historical deployment data;
  - a universal or confirmatory superiority claim;
  - a pure-jump attribution;
  - evidence across exploration levels or learner classes.

### E.3 Diagnostic / mechanism

- **What existed before:** return autocorrelation diagnostics (Lo–MacKinlay) and policy-response plots are standard tools.
- **What this paper adds:** it pairs a target-law lag-conditional diagnostic (mean, variance, fixed-threshold tail) with the executed response of saved policies. It shows that the SBJTS-trained feedback is directionally aligned with the target law's lag structure while the GBM-trained feedback is flat, at almost identical mean exposure.
- **What it does NOT add:** a causal attribution of the performance gap to the lag channel, since no lag-ablation experiment was run.

### E.4 Does the Introduction distinguish the paper?

**No.** The Introduction (three paragraphs, no citations) does not mention Chau–Nguyen–Nguyen, exploratory control, jump-diffusion RL or risk-sensitive RL. It gives no contribution statement.

Proposed 3-bullet contribution statement, for review:

> - **Controlled training-law comparison.** Holding a constrained exploratory actor–critic learner, its budget, constraints and deployment law fixed, we compare training under a history-dependent jump simulator (SBJTS) with training under an iid GBM calibrated to the same historical slice. On the simulated deployment law, SBJTS training yields estimated gains in terminal log wealth and reductions in CVaR log loss under both a long-only and a 50%-capped constraint. Average risky exposure is almost unchanged.
> - **Theory for why the training law matters beyond local moments.** Exact wealth coupling, a constructive non-equivalence result under matched one-step moments or marginals, a trajectory policy gradient for an observation-based policy that does not assume a Markov observation, and a symmetric occupancy/continuation-value identity for the training-law gradient gap (an attribution convention, not a causal decomposition).
> - **Descriptive mechanism evidence.** The target law's lag-conditional mean, variance and tail probability vary strongly with the lagged return, while the GBM control is flat. The SBJTS-trained policies' executed response to lagged return is directionally aligned with that structure, while GBM-trained policies are nearly insensitive to it.

---

## F. Reviewer attacks

See `RL_SBJTS_REVIEWER_ATTACKS_v1.md`.

---

## G. Reference verification (existing bibliography)

| Key | Manuscript entry | Verification | Issues |
|---|---|---|---|
| Merton1969 | R. C. Merton, "Lifetime Portfolio Selection under Uncertainty: The Continuous-Time Case," *Review of Economics and Statistics*, 51(3), 247–257, 1969. | Authors, title, journal, 51(3), 247–257, 1969 confirmed. DOI 10.2307/1926560. | Missing DOI. **Never cited in text.** |
| Merton1971 | R. C. Merton, "Optimum Consumption and Portfolio Rules in a Continuous-Time Model," *Journal of Economic Theory*, 3(4), 373–413, 1971. | Confirmed: JET 3(4), 373–413, December 1971. ScienceDirect PII S002205317190038X, which implies DOI 10.1016/0022-0531(71)90038-X (derived from the PII; confirm before adding). | Missing DOI. **Never cited in text.** |
| Chau2026 | H. Chau, D. Nguyen, and T. Nguyen, "Continuous-time optimal investment with portfolio constraints: A reinforcement learning approach," *EJOR*, 328, 1068–1092, 2026. DOI 10.1016/j.ejor.2025.08.032. | Title, authors' surnames, EJOR, vol. 328, pages 1068–1092, year 2026 confirmed (issue 3). ScienceDirect PII S037722172500671X; arXiv:2412.10692. **The DOI string could not be independently resolved** (Crossref and ScienceDirect blocked by network policy; search did not index it). | Missing issue number (3). Author given names unverified. DOI unverified. **Never cited in text.** |

**Findings:**

- There are no wrong titles, years or venues.
- All three entries are incomplete (missing DOI or issue).
- **Zero in-text citations.** The claims needing citations are listed as NC in section A: I1, I3, B5, D1, T1a/T3a (Williams; Baxter–Bartlett), and R2/CVaR (Rockafellar–Uryasev).
- **No reference is cited for a claim it does not support**, because none is cited at all.

### Sources used for verification

- [Chau–Nguyen–Nguyen, EJOR (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S037722172500671X) · [arXiv:2412.10692](https://arxiv.org/abs/2412.10692)
- [Merton 1969, RePEc](https://ideas.repec.org/a/tpr/restat/v51y1969i3p247-57.html) · [Merton 1969, Wikipedia (DOI)](https://en.wikipedia.org/wiki/Merton's_portfolio_problem)
- [Merton 1971, RePEc](https://ideas.repec.org/a/eee/jetheo/v3y1971i4p373-413.html) · [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/002205317190038X)
- [Merton 1976, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0304405X76900222)
- [Wang–Zariphopoulou–Zhou, JMLR](https://www.jmlr.org/papers/v21/19-144.html) · [Wang–Zhou, Math. Finance](https://onlinelibrary.wiley.com/doi/abs/10.1111/mafi.12281) · [Jia–Zhou, JMLR](https://www.jmlr.org/papers/v23/21-1387.html)
- [Gao–Li–Zhou, arXiv:2405.16449](https://arxiv.org/abs/2405.16449) · [Nguyen–Nkuize, arXiv:2604.22188](https://arxiv.org/abs/2604.22188) · [Dai–Dong–Jia–Zhou, arXiv:2312.11797](https://arxiv.org/pdf/2312.11797) · [Bender–Thuan, arXiv:2312.13409](https://arxiv.org/abs/2312.13409)
- [Cvitanić–Karatzas, Project Euclid](https://projecteuclid.org/journals/annals-of-applied-probability/volume-2/issue-4/Convex-Duality-in-Constrained-Portfolio-Optimization/10.1214/aoap/1177005576.full)
- [Hawkes 1971, Biometrika](https://academic.oup.com/biomet/article-abstract/58/1/83/224809) · [Aït-Sahalia et al., NBER](https://www.nber.org/papers/w15850)
- [Nilim–El Ghaoui, PDF](https://people.eecs.berkeley.edu/~elghaoui/Pubs/RobMDP_OR2005.pdf) · [Iyengar, MOR](https://pubsonline.informs.org/doi/10.1287/moor.1040.0129) · [Zhao et al., Semantic Scholar](https://www.semanticscholar.org/paper/Sim-to-Real-Transfer-in-Deep-Reinforcement-Learning-Zhao-Queralta/5a1b92aa50797a7c1e99b8840ff01aad66038596)
- [Rockafellar–Uryasev, Semantic Scholar](https://www.semanticscholar.org/paper/Optimization-of-conditional-value-at-risk-Rockafellar-Uryasev/58444c142b6ea5c71a435cac7a0b4c66d6c68869) · [Tamar et al., AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/9561) · [Chow et al., NeurIPS](https://proceedings.neurips.cc/paper/2015/hash/64223ccf70bbb65a3a4aceac37e21016-Abstract.html) · [Hambly–Xu–Yang, Math. Finance](https://onlinelibrary.wiley.com/doi/full/10.1111/mafi.12382)
- [Williams 1992, Springer](https://link.springer.com/article/10.1007/BF00992696) · [Baxter–Bartlett, arXiv:1106.0665](https://arxiv.org/abs/1106.0665)
- [Lo–MacKinlay 1988, RFS](https://academic.oup.com/rfs/article-abstract/1/1/41/1601244)

---

## Confirmations

- No experiment, training, evaluation or bootstrap was run.
- No research evidence, frozen artifact, estimand or claim was modified.
- The manuscript was not edited.
- The accepted theory report was not edited.
