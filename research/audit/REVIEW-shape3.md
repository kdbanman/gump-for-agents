# Review of research/shape3/: the second variable at equal area and equal shortest loop

Adversarial review, 2026-11-15. Object: `research/shape3/` at 371993b (forecasts `PREDICTIONS.md` and
`data/predictions.json` at 46baf66, amendments f645b13, 43a5e0e, ffcaf36; write-up `README.md`; `data/`). Code in
`research/audit/shape3/`; bulk output in `research/scratch/audit_shape3/` (git-ignored). Nothing is imported from
`research/shape*/` or `research/audit/shape/`; ts.c / ts3.c are read, never compiled or linked.

**The independent stepper** is `st.c` with its own geometry `geom.py` (written from AUTOMATON.md's doubled-coordinate
offsets, not the cube-index table): bit-sliced, 512 replicas, a half-adder tree for the 12-neighbour count (ts3 uses
carry-save full adders), xoshiro256** soups, renewal lives, **events resolved every generation** (ts3: every 8), and a
**Brent settled test** (snapshot at ages 0, 1, 2, 4, …; any period is caught, the period is logged; censored at the
snapshot age, inside the cycle). Validation: lane 0's whole state, lifted to the cubic N-torus, is identical as a set
of cells to the engine's `--trace` at every generation 0–2,000 on (1,4,12), (1,3,12) (two soups), (1,5,15), (1,4,15),
(2,2,8), (1,6,16) and 0–600 on (2,4,12); a negative control (birth on 4 only) fails at generation 1.

    python3 research/audit/shape3/validate.py 1 4 12 2000 12        # one torus; all: research/audit/shape3/validate.log
    python3 research/audit/shape3/plan.py list                       # run plan, committed in 7ecceb5 before any run
    nohup python3 research/audit/shape3/plan.py lane 0 > research/scratch/audit_shape3/lane0.log 2>&1 &   # ~10 min
    nohup python3 research/audit/shape3/plan.py lane 1 > research/scratch/audit_shape3/lane1.log 2>&1 &   # ~35 min (A = 72)
    python3 research/audit/shape3/ana.py [--all]   # per torus, pair d, settled periods (--all: with zombie-rate jobs)
    python3 research/audit/shape3/enum_check.py    # claim 2 (1 s)
    python3 research/audit/shape3/recount.py       # runs.csv against shape3's raw event files
    python3 research/audit/shape3/capcount.py      # zombie lives in the earlier capped runs
    python3 research/audit/shape3/score_check.py   # loop^2 >= 12 scores, with the T01/T12 covariance and the null
    python3 research/audit/shape3/zombie_check.py  # the period-16 state, period confirmed by the engine

Outputs of each are committed next to the scripts (`*_out.txt`). Plan: seeds 71001–71011 (fixed in 7ecceb5);
seeds 71101–71104 (four extra A = 36 jobs, added in 27d2f85 after the first four Q36 jobs because the zombie counts
per job looked uneven; used only for zombie rates, never in a d).

## Summary

| claim | verdict |
|---|---|
| 1. Sign change below saturation | **stands.** Independently: Q36 **−0.0220 ± 0.0009**, Q45 **+0.0085 ± 0.0014** (theirs −0.0223 ± 0.0007, +0.0076 ± 0.0013). Labels checked: both members of each pair have loop² 9 and Y has the longer second loop. The value does not depend on the check window (per generation, 8-generation rounding, ties either way, settled exposure dropped: all within 0.0002). |
| 2. Structure [proved] | **stands, two small slips.** det = 0.75 n² is an identity; at every n ≤ 28 the 12-element point-group orbits coincide with the Gram classes; Q1 ≥ 12 groups only at A = 48, 60, 72, 84. But A = 72 has one pair and one triple with Q1 ≥ 12, not "two pairs and one triple"; and Q1 = 9 groups also exist at A = 81. |
| 3. Zombie lives | **stands; harmless to every earlier published difference.** (a) a period-16 state on (1,4,12), period confirmed by the engine; (b) about 3.5 × 10⁻⁶ of lives at A = 36 and 4 × 10⁻⁶ at A = 48; (c) at most 0.0004 in ln τ at A = 48 and 0.0007 at A = 60 in any capped run, below every error; (d) ts3's test cannot cut a chaotic life; it misses periods with p / gcd(p, 840) > 128, of which none occurred among 13,000 settled lives here. |
| 4. Nulls at A = 72 | **stands with correction.** Counts reproduce exactly from shape3's raw event files; job scatter matches the errors; no exposure-accounting bias within a pair. One independent st.c job on (2,4,12) gives 14.9765 ± 0.0064 against their 14.9706 ± 0.0029. But T01 and T12 share (2,4,12), correlation −0.5, which the scoring ignores; the README's "≤ 0.4% of face deaths" for firewalls is false on the triple (5.3%). |
| 5. Scoring | **the forecasts were fixed in time; "survives out of sample" does not stand.** Forecasts are unchanged since 46baf66, before any production result; the v1 glimpse could not touch them. Under the committed rule all five candidates are refuted. On the post hoc loop² ≥ 12 split the null "d = 0 at A = 72" fits better (χ² 2.4 / 3) than K2 (4.3) or K3 (5.2), and with the T01/T12 covariance K3 has p 0.036 and K2 p 0.086. |
| 6. Other | Estimator and 8-generation window: no bias in d (checked against per-generation resolution). Firewall definition on the twisted tori agrees with an own derivation. Amendment timing text inaccurate (see corrections). |

## Claim 1: the sign change below saturation

This review's runs (`ana.py`, plan seeds 71001–71008; 2 jobs per torus, 2 × 10⁶ generations × 512 at A = 36,
5 × 10⁶ × 512 at A = 45; no cap; 4 × 10⁹ resp. 5 × 10⁹ life-generations per torus):

| torus | F | W | X (same generation) | S | ln τ_face, per generation | 8-gen rounding, ties as face | shape3 "ties as face" |
|---|---:|---:|---:|---:|---|---:|---:|
| (1,4,12) | 2,484,818 | 13,183 | 3,451 | 3,167 | 7.4076 ± 0.0006 | 7.4104 | 7.4102 |
| (1,3,12) | 2,540,084 | 14,056 | 3,477 | 3,026 | 7.3856 ± 0.0006 | 7.3886 | 7.3877 |
| (1,5,15) | 963,737 | 21,564 | 1,010 | 184 | 9.2710 ± 0.0010 | 9.2706 | 9.2698 |
| (1,4,15) | 955,602 | 21,617 | 963 | 208 | 9.2795 ± 0.0010 | 9.2791 | 9.2775 |

| pair | per generation | 8-gen rounding | ties as face | settled exposure removed | shape3 |
|---|---|---|---|---|---|
| Q36 (1,4,12) → (1,3,12) | **−0.0220 ± 0.0009** | −0.0219 | −0.0220 | −0.0219 | −0.0223 ± 0.0007 |
| Q45 (1,5,15) → (1,4,15) | **+0.0085 ± 0.0014** | +0.0085 | +0.0085 | +0.0084 | +0.0076 ± 0.0013 |

Both agree (0.3σ and 0.5σ). The per-torus values agree with shape3's once the same conventions are applied (per
generation the values are 0.003–0.004 lower at A = 36, because an 8-generation window adds about 3.5 generations to
every life and moves face-then-firewall lives into X; the shift is common to both members). Grams (`enum_check.py`):
(1,4,12) (9, 0, 12), (1,3,12) (9, 6, 13); (1,5,15) (9, 3, 19), (1,4,15) (9, 9, 21). No mislabel; the sign of Q36
is real: the face with the longer second loop dies sooner at A = 36, later at A = 45.

Incidental: P1 (one job per torus, seeds 71009–71010) +0.0109 ± 0.0032, against shape3's +0.0144 ± 0.0019 (1σ).

## Claim 2: the structure

`enum_check.py` (own HNF enumeration, own brute-force reduction, point group found by searching integer matrices
that preserve x² + xy + y²): for n = 1 … 28, Q1·Q2 − B² = 0.75 n² for every lattice (an identity: the form has
determinant 3/4 and the index is n), and the partition of the HNFs into point-group orbits equals the partition by
reduced Gram matrix at every n. Groups of ≥ 2 classes with equal Q1:

- Q1 ≥ 12: A = 48 (one pair), 60 (two pairs: Q1 12, 16), 72 (a pair at Q1 12 and a triple at Q1 16), 84 (two pairs).
  None at 54, 63, 66, 75, 78, 81. The README's "two pairs and one triple at 72" is wrong: one pair and one triple.
- Q1 = 9: A = 36, 45, 54, 63, 72 **and 81**.

So "one number fixes the lattice", "class = Gram class at n ≤ 28" and the list of Q1 ≥ 12 groups are right.

## Claim 3: zombie lives

**(a) A state.** `zombie_1_4_12_p16.txt`: 42 live cells on (1,4,12), period 16 (16 ∤ 840), found by st.c (seed
71001) and confirmed by the engine on the cubic 12-torus lift (`zombie_check.py`: "periodic, period 16, cycle start
0"). Other periods not dividing 840 seen: 9, 11, 13, 16, 19, 22, 48, 52 (A = 36), 13 (A = 45), 9 (A = 48); the
engine confirms 16, 19 and 13 on (1,3,12) as well.

**(b) How often.** A life ends in a cycle whose period does not divide 840 in **35 of 1.01 × 10⁷ lives at A = 36
(3.5 × 10⁻⁶; 15 on (1,3,12), 20 on (1,4,12))**, 1 of 2.0 × 10⁵ at A = 48 here, and 9 of 2.14 × 10⁶ A = 48
loop² ≥ 7 lives in the review of shape2 (lives reaching its cap, or open at job end older than 20 mean lives,
`capcount.py`): **about 4 × 10⁻⁶ at A = 48**. At A = 45, 1 of 9.4 × 10⁵. This matches the README's v1 job: at
3.2–4 × 10⁻⁶ per life, 512 replicas × ~9,000 lives give 14–19 replicas holding a zombie at the end; they report 14.
The counts per A = 36 job are overdispersed on (1,3,12) (11, 0, 3, 1; χ² 20 on 3) and not on (1,4,12) (7, 1, 5,
7); I have no explanation, and the rates above are means over all jobs.

**(c) Bias in the earlier capped measurements.** A zombie adds at most min(cap, rest of job) of exposure with no
event; the most it can shift ln τ is ln(E / (E − zombie exposure)).

- Review of shape2 (ts.c, renewal, cap 5 × 10⁵), counted directly from its event files at A = 48, where a chaotic
  life cannot reach 50 mean lives: zombie exposure share ≤ 3.7 × 10⁻⁴ on every torus, shift ≤ +0.0004. P1:
  +0.0003 on (2,2,8), +0.0002 on (1,6,16), so the pair difference moves by 0.0001 (error ± 0.0021).
- A = 60 (same review; research/shape, cap 5 × 10⁵): honest lives reach the cap there (mean life 1.3 × 10⁵), so
  zombies cannot be counted. Upper bound: every settled life of shape3's cap-free A = 60 jobs (S, which includes
  all zombies ts3 catches, and ts3 leaves no long open life) carried a full cap: (S / E) × 5 × 10⁵ = 0.0005 (1,8,20),
  0.0007 (2,2,10), 0.0002 (1,5,20). Errors of the published A = 60 differences: ± 0.0028–0.0049.
- research/shape2's own runs (one life per replica, caps 16,384 at A = 48, 65,536 at A = 60): rate × cap / mean
  life ≈ 4 × 10⁻⁶ × 2 ≈ 10⁻⁵ at A = 48; ≤ 0.0002 at A = 60 by the bound above.
- A = 72 (caps 5 × 10⁵ or less, mean life 1.5 × 10⁶): (S / E) × cap ≤ 10⁻⁵.

**No published difference in research/shape, research/shape2 or the review of shape2 can move by more than 0.0007,
which is below every quoted error.** The README's "do little harm" is right and can be made quantitative.

**(d) ts3's test.** Read in ts3.c: a lane is censored only when its whole state equals a snapshot taken at
840(c − m) with born < 840(c − m) strictly; the snapshot of the check where a lane is reseeded is written before the
reseed, and the strict inequality excludes it; ring slots (c − m) mod 129 for m ≤ 128 are distinct from slot c,
written after the comparisons. Exact equality in the same life proves the orbit periodic, so **no chaotic life can
be cut.** Its censor time (the most recent matching snapshot) lies in the cycle, at most a few × 840 generations
after cycle entry; zero-hazard exposure of this kind is ≤ the S lives' share, which removing entirely moves no d by
more than 0.0003 (claim 1, "settled exposure removed"). **What it misses**: periods with p / gcd(p, 840) > 128
(e.g. 131, 137, 143 = 11·13, …), and cycles entered less than 840·m generations before the job ends (these are
open lives, short by construction). The largest period among the 12,968 settled lives of this review's runs is 52
(m = 13); none would have escaped.

## Claim 4: the nulls at A = 72

- **Counts.** `recount.py` recounts all 35 rows of `data/runs.csv` from shape3's raw event files
  (`research/scratch/shape3/ev_*.txt`): exposure, F, X, W, S, C, open identical in every row. Per-torus sums give the
  README table exactly (its "mean life" divides by all lives, open included).
- **Job scatter.** ln τ per job against the torus mean: χ² 7.8 / 4 (1,6,24), 2.6 / 4 (2,4,12), 3.4 / 4 (1,5,24),
  0.4 / 1 and 0.5 / 1 (N72), 0.5 / 1 and 1.1 / 1 (Q63). The quoted ± 1/√F is consistent with the job scatter.
- **Accounting.** Both members of each pair have the same job length, replica count, check window and soup; lives
  open at job end are ≤ 9 mean lives at A = 72 (oldest 1.3 × 10⁷ against 1.5 × 10⁶) and are 2% of lives; with a
  near-constant hazard (young/old split within error) censoring at job end is uninformative. Firewalls, the
  competing end, are 5.3%, 5.3%, 5.4% of face deaths on the triple and 0 on N72, and equal within their Poisson noise, so
  as a competing end they treat the members alike. Ties change no d by more than 0.0001. I find no bias above 0.001.
- **Correlation.** T01 = (2,4,12) − (1,6,24) and T12 = (1,5,24) − (2,4,12) share (2,4,12): correlation −0.50. The
  committed scoring and the README's split treat them as independent (claim 5).
- **Independent job.** One st.c job on (2,4,12), 7.5 × 10⁷ generations × 512, seed 71011: F 24,053, W 1,270 (5.3%), X 1, S 0;
  **ln τ_face = 14.9765 ± 0.0064**, against shape3's 14.9706 ± 0.0029 over five jobs (+0.0059 ± 0.0071, 0.8σ;
  per-generation and 8-generation conventions agree to 0.0001 here). Their stepper lands within error of mine.
- **Firewall share.** The README's "Firewalls (W), ties (X) and settled lives (S) are ≤ 0.4% of face deaths on every
  loop² ≥ 12 torus" is false for the triple: W is 5.3% of F on (1,6,24), (2,4,12), (1,5,24) (`data/runs.csv`).

## Claim 5: the scoring

- **Fixed before the data.** `predict3.py`, `data/predictions.json` and `data/predictions.txt` have one commit each,
  46baf66 (20:44:40), and are unchanged at HEAD. All v2 production event files are later (first: 20:50:15). The
  v1 jobs (Q36, Q45; seeds 30001–30004) ran between 46baf66 and f645b13 (20:49:16, 4.5 minutes later — not "about
  25 minutes" as the amendment says), and their numbers were seen and disclosed; the forecasts did not change, and
  the v2 Q36/Q45 values come from fresh seeds. The amendment's line "On the Q36 job it removed every zombie (0 open
  lives older than 20,000 …, 106 more lives settled)" was committed before the v2 Q36 file existed, so it refers to a
  test rerun that is not in the record. The plan changes after v1 (settled test, budget, order) touch every torus
  alike and do not depend on which way Q36 or Q45 came out. I judge the scoring of the committed forecasts fair.
- **Under the committed rule all five candidates are refuted** (χ² 111–1246 on 7). The README says so.
- **"Survives out of sample at loop² ≥ 12" is not fair.** The split is post hoc, it keeps the three differences on
  which every decaying candidate forecasts ≤ 0.003 against errors of 0.004–0.006, and on those three the null fits
  best (`score_check.py`):

  | on T01, T12, N72 | treated as independent (README) | with the T01/T12 covariance |
  |---|---|---|
  | K2 | 4.3 / 3, p 0.23 | 6.6 / 3, p 0.086 |
  | K3 | 5.2 / 3, p 0.16 | 8.6 / 3, p 0.036 |
  | d = 0 at A = 72 | 2.4 / 3, p 0.50 | 2.9 / 3, p 0.41 |
  | K1, K1a, K3b | 15.7–23.7, p ≤ 0.0013 | 26.5–40.5, p ≤ 8 × 10⁻⁶ |

  What the A = 72 data establish is negative: the size-free candidates are excluded, and the equal-loop effect at
  A = 72 is below about 0.008 (2σ). K2 and K3 are consistent with that only because they forecast nearly zero.
  The README's own paragraph below the table says much of this; the table's "survives" and the verdict line should
  match it.
- **Sentence I accept**: "Under the committed rule all five candidates are refuted. On the three loop² ≥ 12
  differences alone (a split chosen after the data, not in PREDICTIONS.md), K2 and K3 are not rejected (χ² 6.6 and
  8.6 on 3 with the T01/T12 covariance, p 0.09 and 0.04), but 'no equal-loop effect at A = 72' fits better (χ² 2.9 on
  3); these data exclude the size-free candidates K1, K1a and K3b and cannot tell K2 or K3 from zero."

## Claim 6: other points

- **Window and ties.** Resolving events every generation instead of every 8 changes ln τ by −0.004 at A = 36 and
  −0.0001 at A = 45 per torus, and no pair difference by more than 0.0001 (claim 1). shape3's statement that the
  window does not bias the pairs stands.
- **Face death and firewall on a twisted torus.** geom.py derives the transverse layer index s_d = d·p mod P_d,
  P_d = gcd of d·(2g) over the generators, independently; every in-slab neighbour pair steps by ≤ 2 layers (T1);
  diagonals with fewer than 3 layers carry no firewall (three consecutive of two layers would be total death). The
  resulting W and X rates match ts3's once the window is accounted for. Face death = a boundary {111} layer all dead,
  permanent by T2. No disagreement.
- **Estimator.** ln(2E/F) ± 1/√F is the cause-specific face hazard per face; firewalls and settling censor it. Under
  the near-constant hazard seen here this is unbiased, and it is the same estimator for both members.
- **Open lives.** The README's "no open life older than about 12 mean lives" should read 13.5 ((1,5,18): 380,624
  against 28,217); the age tail of that torus's 6 × 10⁵ lives is exponential (26 lives beyond 10 mean lives, 27
  expected), so it is not a zombie.

## Corrections the write-up needs

1. Verdict, candidates table and the paragraph after it: replace "survives out of sample at loop² ≥ 12" (K2, K3) by
   the sentence in claim 5: "Under the committed rule all five candidates are refuted. On the three loop² ≥ 12
   differences alone (a split chosen after the data, not in PREDICTIONS.md), K2 and K3 are not rejected (χ² 6.6 and
   8.6 on 3 with the T01/T12 covariance, p 0.09 and 0.04), but 'no equal-loop effect at A = 72' fits better (χ² 2.9
   on 3); these data exclude the size-free candidates K1, K1a and K3b and cannot tell K2 or K3 from zero."
2. Scoring: add "T01 and T12 share (2,4,12) and are correlated (−0.5); the χ² values treat the seven differences as
   independent. This changes no verdict under the committed rule."
3. "Why the experiment can only separate candidates by size": "two pairs and one triple at 72" → "one pair (Q1 = 12)
   and one triple (Q1 = 16) at 72, two pairs at 60 and at 84"; "Q1 = 9 groups exist at A = 36, 45, 54, 63, 72" →
   "… 63, 72 and 81".
4. Per torus: "Firewalls (W), ties (X) and settled lives (S) are ≤ 0.4% of face deaths on every loop² ≥ 12 torus and
   on Q36" → "Ties and settled lives are ≤ 0.4% of face deaths on every torus; firewalls are ≤ 0.4% on Q36, P1, P3
   and N72, 5.3% on the A = 72 triple (equal on all three members), 2% on Q45, 14% on Q54, 98% on Q63."
5. Set-up, zombie lives: add "They are rare: 3.5 × 10⁻⁶ of lives at A = 36 and about 4 × 10⁻⁶ at A = 48 (review of
   shape3). In the earlier capped runs they shift ln τ by at most 0.0004 at A = 48 and 0.0007 at A = 60, below every
   quoted error." "No open life older than about 12 mean lives" → "13.5".
6. PREDICTIONS.md amendment (or a note in the README): "about 25 minutes after the commit above" → "4.5 minutes
   after (20:49 against 20:44)"; the "106 more lives settled" test run is not in the record.
7. Verdict, Q36/Q45: add "confirmed with an independent stepper resolving events every generation: −0.0220 ± 0.0009
   and +0.0085 ± 0.0014 (research/audit/REVIEW-shape3.md)", and drop "No second stepper for these numbers" from "Not
   checked" for Q36 and Q45.

## Not checked

- Q54, Q63, P2, P3, N72 and the A = 72 triple were not rerun, except one job on (2,4,12); the A = 72 nulls rest on
  shape3's counts (verified against its raw files) plus that one job.
- The post hoc material (`explore3.py`: refits, near-firewall rates, rows), the age-bin tables (`agebins.csv`) and
  the h-dependence summary were not recomputed.
- Zombie rates at A ≥ 54 were not measured; the bias bounds there use shape3's settled counts as an upper limit.
- Event detection in st.c (face, firewall, settled) is not validated against the engine, only the stepping is; it
  agrees with ts3's counts once the window convention is matched, and the zombie periods agree with the engine.
- The overdispersion of zombie counts per job on (1,3,12) is unexplained.
- `research/audit/shape3_lead_check.py` (the lead's arithmetic from runs.csv) was not repeated.
