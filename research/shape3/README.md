# The second variable: equal area, equal shortest loop, different lifetime

2026-11-14. research/shape2 found that two periodic slab faces with the same area A and the same shortest loop can
differ in ln τ_face (by 0.015 at A = 48 and 0.014 at A = 60, the one with the shorter second loop dying sooner).
This experiment asks what the second variable is: five candidate formulas, each fitted on the three known pairs
only, forecast every new equal-area, equal-loop pair (`PREDICTIONS.md`, committed in 46baf66 before any production
run; amendments f645b13, 43a5e0e, ffcaf36, also before the results they concern; two inaccuracies in the first amendment are noted at the end of
PREDICTIONS.md). Statements are marked [proved],
[measured] or [conjectured]; "post hoc" means looked for after the data.

## Reviewed

An adversarial review, `research/audit/REVIEW-shape3.md` (code and outputs in `research/audit/shape3/`), checked
this write-up with its own stepper (`st.c`, own geometry, events resolved every generation, a Brent settled test;
validated against the engine's `--trace` as a set of cells for 2,000 generations on seven tori and 600 on
(2,4,12)). What it
confirmed independently [measured]:

- Q36 **−0.0220 ± 0.0009** and Q45 **+0.0085 ± 0.0014** from fresh runs (here −0.0223 ± 0.0007 and
  +0.0076 ± 0.0013; 0.3σ and 0.5σ), with no dependence on the check window or on ties beyond 0.0002.
- Every count in `data/runs.csv` (exposure, F, X, W, S, open; all 35 rows), recounted from the raw event files
  (`recount.py`); the job scatter matches the quoted ± 1/√F.
- One independent job at A = 72, on (2,4,12): ln τ_face = 14.9765 ± 0.0064 against 14.9706 ± 0.0029 here (0.8σ).
- The structure section (with two corrections, applied below), the zombie mechanism (a period-16 state on
  (1,4,12), confirmed by the engine) and that the forecasts were fixed before any production result.

It also corrected the scoring of K2 and K3 at loop² ≥ 12 (they do not "survive"; see Verdict), the firewall share
at A = 72, the list of equal-loop groups, and the age of the oldest open life; these corrections are applied in
this text. What it did not rerun is listed under "Not checked".

## Verdict

- **[measured] At A = 72 the equal-loop differences vanish.** The three new differences with shortest loop² ≥ 12
  are T01 = −0.0062 ± 0.0041, T12 = +0.0005 ± 0.0041 and N72 = +0.0018 ± 0.0061, all zero within 1.5σ, where the same
  kind of pair differs by +0.015 at A = 48 (re-measured here cap-free: +0.0144 ± 0.0019) and by +0.014 at A = 60.
  The shape term between *different* shortest loops grows with area (+0.06 at 60, +0.10 at 72, research/shape2);
  the term at *equal* shortest loop does not.
- **[measured] Below saturation (shortest loop² 9) the differences are large and change sign.** Q36 (A = 36):
  **−0.0223 ± 0.0007**, the face with the *longer* second loop dying sooner, 30σ; Q45 (A = 45): +0.0076 ± 0.0013;
  Q54 (A = 54): −0.0020 ± 0.0019; Q63 (A = 63): +0.0017 ± 0.0020. No candidate forecast a negative difference
  anywhere. Q36 and Q45 are confirmed with an independent stepper resolving events every generation: −0.0220 ±
  0.0009 and +0.0085 ± 0.0014 (research/audit/REVIEW-shape3.md).
- **Candidates** (forecast parameters fitted on the three known pairs only, `PREDICTIONS.md`; scored on six new
  differences):

  | candidate | committed score (7 differences) | loop² ≥ 12 alone (3) | loop² 9 alone (4) | verdict |
  |---|---|---|---|---|
  | K1 second loop, linear | χ² 1246, p 10⁻²⁶⁴ | 23.7, p 3 × 10⁻⁵ | 1223 | **refuted**, in both sets |
  | K1a angle, linear | 834, p 10⁻¹⁷⁵ | 15.7, p 0.0013 | 818 | **refuted**, in both sets |
  | K3b cos 2π Re τ, size-free | 874, p 10⁻¹⁸⁴ | 18.3, p 4 × 10⁻⁴ | 856 | **refuted**, in both sets |
  | K2 loop sum Σ e^{−1.41 \|v\|}, amplitude ∝ A | 111, p 5 × 10⁻²¹ | 4.3, p 0.23 (6.6, p 0.086 with the T01/T12 covariance) | 107 | **refuted** by the committed rule (Q36 −9σ, Q45 +4σ); at loop² ≥ 12 alone not rejected, but not distinguishable from zero |
  | K3 modular e^{−2πh} cos 2π Re τ | 896, p 10⁻¹⁸⁹ | 5.2, p 0.16 (8.6, p 0.036 with the covariance) | 891 | **refuted** by the committed rule (Q36 −30σ, Q45 +4σ); at loop² ≥ 12 alone not rejected, but not distinguishable from zero |
  | d = 0 at A = 72 (not a committed candidate; for comparison) | — | 2.4, p 0.50 (2.9, p 0.41 with the covariance) | — | fits the loop² ≥ 12 differences best |
  | firewall cut, short rows, layer count, number of shortest loops, "shorter third loop dies sooner" | — | — | — | refuted in-sample, before the runs |

  Under the committed rule all five candidates are refuted. On the three loop² ≥ 12 differences alone (a split
  chosen after the data, not in PREDICTIONS.md), K2 and K3 are not rejected (χ² 6.6 and 8.6 on 3 with the T01/T12
  covariance, p 0.09 and 0.04), but 'no equal-loop effect at A = 72' fits better (χ² 2.9 on 3); these data exclude
  the size-free candidates K1, K1a and K3b and cannot tell K2 or K3 from zero. T01 and T12 share the torus (2,4,12)
  and are correlated at −0.5. What the A = 72 data establish is negative: the size-free forms, which forecast
  0.007–0.015 at A = 72, are excluded, and the equal-loop effect at A = 72 is below about 0.008 (2σ). K2 and K3
  (which forecast within 0.001 of each other everywhere tested) are consistent with that only because they
  forecast ≤ 0.003 there; that the effect decays with h = Im τ, as both say, is [conjectured], not tested. Below
  saturation both fail.
  If anything the rectangular (1,6,24) lives longest at A = 72 (T01 −1.5σ, T02 = −0.0056 ± 0.0041), the opposite
  of A = 48 and 60, where the rectangular member dies sooner; not significant.
- **What the second variable is: still not found.** At these sizes every candidate is a function of one number per
  group ([proved], next section), so "which variable" reduces to "which function of x, h and A". Two facts constrain
  it: the effect is about 0.015 at h ≈ 1.1 (A = 48, 60), smaller at h = 1.44 (P3: +0.0069 ± 0.0024 pooled), ≈ 0
  at h = 1.3 and 1.73 (A = 72); and at shortest loop² 9 it is not even of one sign (−0.022 at A = 36, h = 1.155).


## Why the experiment can only separate candidates by size [proved]

Reduced Gram matrix of the period lattice (Q1, 2B, Q2): Q1 = shortest loop², Q2 = second loop², 0 ≤ B ≤ Q1/2
(Q = x² + xy + y², research/shape/lattice.py). The determinant Q1·Q2 − B² = 0.75 n² (n = A/3) is fixed by the area.
So within a group of equal A and Q1 the lattice up to isometry is fixed by one number, Q2, or B, or the angle, or
the third loop Q3 = Q1 + Q2 − 2B (which falls as Q2 rises), or x = Re τ = B/Q1 of the shape modulus
τ = (B + i√D)/Q1, whose imaginary part h = √D/Q1 is fixed. Every candidate that sees only the flat torus (loop
lengths, theta series, angle, number of shortest loops) is a function of x within a group. More: at every index
n ≤ 28 (A ≤ 84) no two classes share a Gram matrix (checked by enumeration), so the class itself, and with it every
lattice-scale quantity (rows, transverse layers, firewall cuts), is a function of the Gram matrix. At these sizes
no experiment can separate "metric" from "lattice-scale" candidates; only the form of the function of x (and of A
and h) can be tested. And the equal-loop groups with Q1 ≥ 12
are few: at A ≤ 84 they occur only at A = 48, 60, 72 and 84 (none at 54, 63, 66, 75, 78 or 81): one pair at 48,
one pair (Q1 = 12) and one triple (Q1 = 16) at 72, two pairs at 60 and at 84. Below saturation, Q1 = 9 groups
exist at A = 36, 45, 54, 63, 72 and 81. (Rechecked independently: `python3 research/audit/shape3/enum_check.py`.)

## Set-up

- **Stepper.** `ts3.c` is the review's independent stepper (`research/audit/shape/ts.c`: bit-sliced, renewal lives,
  own RNG and layer indexing) with two changes: a carry-save AVX-512 step kernel (4.4× faster; the rule is the
  same), and a stronger settled test (below). **Validation [measured]**: on all 19 tori of the plan, population ×
  copies equals the engine's on the cubic N-torus (N = index) at each of 4,000 generations, through the vector
  kernel; and ts3 built with ts.c's settled test writes event files identical to the unmodified ts.c (512 replicas,
  60,000 generations, every torus). A negative control (rule broken in the vector kernel) fails at generation 1.
  `bash research/shape3/validate3.sh` → `data/validate.log`.
- **Lives.** 512 replicas, each running successive lives from a fresh 0.4 soup; a life ends at its first event (face
  death F, transverse firewall W, both at the same check X), or is censored when it settles (S) or when its job
  ends (open). **No cap on age.** Events every 8 generations. ln τ_face = ln(2E/F) ± 1/√F; "ties as face" counts X
  as face deaths too.
- **Zombie lives (found here).** Without a cap, lives that settle into a state whose period does not divide 840
  (ts.c compares only with the state 840 generations earlier) keep adding exposure until the end of the job. In
  the first cap-free job of (1,4,12) at A = 36, 14 of 512 replicas held such a life at the end, with ages up to
  7 × 10⁶ against a mean life of 800, carrying 1.7% of the exposure. With the caps of earlier work
  (6.5 × 10⁴, 5 × 10⁵) such lives end as "cap" and do little harm. They are rare [measured, review of shape3]:
  3.5 × 10⁻⁶ of lives at A = 36 (35 of 1.01 × 10⁷; `python3 research/audit/shape3/ana.py --all`) and about
  4 × 10⁻⁶ at A = 48 (`python3 research/audit/shape3/capcount.py` on the review of shape2's event files, with
  `ana.py`). In the earlier capped runs they shift ln τ by at most 0.0004 at A = 48 (counted directly,
  `capcount.py`) and 0.0007 at A = 60 (an upper bound from shape3's settled counts, REVIEW-shape3.md claim 3c),
  below every quoted error. ts3 compares the state with snapshots 840·m generations back in the same
  life, m = 1 … 128, and censors at the first match. Exact equality proves periodicity, so no chaotic life is cut.
  After the change, no torus has an open life older than about 13.5 mean lives ((1,5,18): 380,624 against a mean
  life of 28,217; `data/runs.csv`, column `open`; the oldest ages were checked from the event files).
- **Plan** (`run3.py list`): seeds 31001–31062, fixed before the runs. Wall time is the only stopping rule. The
  machine was shared with other jobs and gave each of the two lanes 20–60% of a core, so the plan was cut short:
  see "What was run".

## What was run

All of plan v2's jobs before the A = 72 rounds (one job per torus at A = 36, 45, 48, 54 and for P3), and A = 72
all five planned rounds of the triple and both rounds of N72 (19 jobs), then Q63 (two jobs per torus). Not run: the cap-free rerun of P2 (queued last; the machine was shared,
the lanes got 20–75% of a core); one P2 job of (1,5,20) finished before the lanes were stopped and gives
12.4729 ± 0.0020 (the review's 12.4735 ± 0.0020); its partner was not run, so P2 has no new difference. The
extension rounds were not reached. Each A = 72 job is 7.5 × 10⁷ generations × 512 replicas. Per-job counts: `data/runs.csv`.

## Per torus [measured]

`python3 research/shape3/analyze3.py report` (first table; also in `data/report.txt`).

| torus | A | jobs | exposure | F | W | X (ties) | open | ln tau_face | ties as face | mean life |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| (1,3,12) | 36 | 1 | 3.835e+09 | 4,727,070 | 20,900 | 19488 | 512 | 7.3918 ± 0.0005 | 7.3877 | 803 |
| (1,4,12) | 36 | 1 | 3.835e+09 | 4,622,363 | 19,155 | 18356 | 512 | 7.4141 ± 0.0005 | 7.4102 | 822 |
| (1,4,15) | 45 | 1 | 6.144e+09 | 1,145,176 | 24,403 | 3721 | 512 | 9.2808 ± 0.0009 | 9.2775 | 5,233 |
| (1,5,15) | 45 | 1 | 6.144e+09 | 1,153,866 | 24,211 | 3972 | 512 | 9.2732 ± 0.0009 | 9.2698 | 5,194 |
| (1,6,16) | 48 | 1 | 5.760e+09 | 555,090 | 0 | 6 | 512 | 9.9404 ± 0.0013 | 9.9404 | 10,360 |
| (2,2,8) | 48 | 1 | 5.760e+09 | 563,155 | 412 | 286 | 512 | 9.9260 ± 0.0013 | 9.9255 | 10,202 |
| (1,5,18) | 54 | 1 | 1.706e+10 | 527,019 | 75,416 | 1820 | 512 | 11.0784 ± 0.0014 | 11.0750 | 28,217 |
| (3,0,6) | 54 | 1 | 1.706e+10 | 525,977 | 74,905 | 1815 | 512 | 11.0804 ± 0.0014 | 11.0770 | 28,290 |
| (1,5,20) | 60 | 1 | 3.264e+10 | 249,958 | 1,103 | 89 | 512 | 12.4729 ± 0.0020 | 12.4725 | 129,690 |
| (1,8,20) | 60 | 1 | 2.304e+10 | 186,263 | 19 | 13 | 512 | 12.4187 ± 0.0023 | 12.4187 | 123,322 |
| (2,2,10) | 60 | 1 | 2.304e+10 | 184,871 | 0 | 0 | 512 | 12.4262 ± 0.0023 | 12.4262 | 124,263 |
| (1,6,21) | 63 | 2 | 9.509e+10 | 495,056 | 484,881 | 1825 | 1024 | 12.8588 ± 0.0014 | 12.8551 | 96,754 |
| (1,7,21) | 63 | 2 | 9.509e+10 | 494,230 | 485,346 | 1830 | 1024 | 12.8605 ± 0.0014 | 12.8568 | 96,789 |
| (1,5,24) | 72 | 5 | 1.920e+11 | 120,906 | 6,471 | 49 | 2560 | 14.9711 ± 0.0029 | 14.9707 | 1,477,082 |
| (1,6,24) | 72 | 5 | 1.920e+11 | 120,229 | 6,361 | 44 | 2560 | 14.9768 ± 0.0029 | 14.9764 | 1,486,103 |
| (1,10,24) | 72 | 2 | 7.680e+10 | 53,171 | 0 | 0 | 1024 | 14.8763 ± 0.0043 | 14.8763 | 1,417,053 |
| (2,2,12) | 72 | 2 | 7.680e+10 | 53,269 | 0 | 0 | 1024 | 14.8745 ± 0.0043 | 14.8745 | 1,414,521 |
| (2,4,12) | 72 | 5 | 1.920e+11 | 120,971 | 6,370 | 51 | 2560 | 14.9706 ± 0.0029 | 14.9702 | 1,477,457 |

Agreement with earlier, independent data (different seeds and codes, all capped): (2,2,8) 9.9260 ± 0.0013 here,
9.9254 ± 0.0015 in the review of shape2, 9.9243 ± 0.0020 in shape2; (1,6,16) 9.9404 / 9.9410 / 9.9384;
(1,8,20) 12.4187 ± 0.0023 / 12.4220 / 12.4148; (2,2,10) 12.4262 / 12.4270 / 12.4223; at A = 72 research/shape's
single runs (± 0.014) gave 14.984 (1,6,24), 14.968 and 14.974 (two presentations of (2,4,12)), 14.965 (1,5,24),
14.875 (2,2,12), 14.878 (1,10,24). The capped earlier values agree with these cap-free ones within their errors.

Ties (X, face death and firewall at the same 8-generation check) and settled lives (S) are ≤ 0.4% of face deaths
on every torus; firewalls (W) are ≤ 0.4% on Q36, P1, P3 and N72, 5.3% on the A = 72 triple (equal on all three
members), 2% on Q45, 14% on Q54 (cut 108), 98% on Q63, equal within each pair. Counting ties as face deaths moves no difference by more than 0.0005, so the
8-generation check window does not bias the pairs compared (and both members of a pair have the same window).

## Pair differences [measured]

d = ln τ_face(Y) − ln τ_face(X), Y the class with the longer second loop; error √(1/F_X + 1/F_Y). "young" and
"old": lives younger / older than 65,536 generations (A ≤ 60; about 0.5–6 mean lives) or 1,048,576 (A = 72, about
0.7 mean lives).

| pair | X -> Y | d | ties as face | young (< 65,536; A = 72: < 1,048,576) | old |
|---|---|---|---|---|---|
| P1 | (2, 2, 8) → (1, 6, 16) | **+0.0144 ± 0.0019** | +0.0149 | +0.0143 ± 0.0019 | +0.0634 ± 0.0462 |
| P3 | (1, 8, 20) → (2, 2, 10) | **+0.0075 ± 0.0033** | +0.0076 | +0.0102 ± 0.0051 | +0.0056 ± 0.0043 |
| T01 | (1, 6, 24) → (2, 4, 12) | **-0.0062 ± 0.0041** | -0.0062 | -0.0088 ± 0.0057 | -0.0034 ± 0.0058 |
| T12 | (2, 4, 12) → (1, 5, 24) | **+0.0005 ± 0.0041** | +0.0006 | +0.0097 ± 0.0057 | -0.0090 ± 0.0058 |
| T02 | (1, 6, 24) → (1, 5, 24) | **-0.0056 ± 0.0041** | -0.0057 | +0.0010 ± 0.0057 | -0.0124 ± 0.0058 |
| N72 | (2, 2, 12) → (1, 10, 24) | **+0.0018 ± 0.0061** | +0.0018 | +0.0041 ± 0.0085 | -0.0007 ± 0.0089 |
| Q36 | (1, 4, 12) → (1, 3, 12) | **-0.0223 ± 0.0007** | -0.0225 | -0.0223 ± 0.0007 | — |
| Q45 | (1, 5, 15) → (1, 4, 15) | **+0.0076 ± 0.0013** | +0.0078 | +0.0076 ± 0.0013 | — |
| Q54 | (3, 0, 6) → (1, 5, 18) | **-0.0020 ± 0.0019** | -0.0020 | -0.0015 ± 0.0021 | -0.0067 ± 0.0062 |
| Q63 | (1, 6, 21) → (1, 7, 21) | **+0.0017 ± 0.0020** | +0.0017 | +0.0017 ± 0.0020 | — |

P1 and P3 are the known pairs, re-measured cap-free (in-sample for every candidate). Pooled with the earlier values
(research/audit/REVIEW-shape2.md): **P1 +0.0148 ± 0.0013, P3 +0.0069 ± 0.0024** (2.9σ; it was 1.8σ). The age
dependence the review hinted at (difference growing with age, 2σ, on P2) is not seen in P1: by age bin +0.016 ±
0.007, +0.018 ± 0.004, +0.012 ± 0.003, +0.015 ± 0.004 for ages 256–1k, 1k–4k, 4k–16k, 16k–65k (the mean life is
10⁴). P2 itself was not rerun. All age bins: `analyze3.py report`, last block.

## Forecasts scored

Committed rule: z = (measured − forecast)/√(σ_m² + σ_f²), hit if |z| < 2; refuted if Σz² over the new differences
has p < 0.01. T01 and T12 share (2,4,12) and are correlated (−0.5); the χ² values treat the seven differences as
independent. This changes no verdict under the committed rule. (With the covariance, the loop² ≥ 12 values in the
second table become 6.6 for K2 and 8.6 for K3, see Verdict; `python3 research/audit/shape3/score_check.py`.)

| candidate | T01 | T12 | N72 | Q36 | Q45 | Q54 | Q63 | chi2 / dof | p | hits | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1_l2 | +0.0051 (-2.7σ) | +0.0152 (-3.4σ) | +0.0152 (-2.1σ) | +0.0051 (-34.5σ) | +0.0101 (-1.6σ) | +0.0051 (-3.5σ) | +0.0101 (-3.8σ) | 1246.3 / 7 | 6.8e-265 | 1/7 | refuted |
| K1a_angle | +0.0075 (-3.3σ) | +0.0070 (-1.6σ) | +0.0111 (-1.5σ) | +0.0111 (-28.1σ) | +0.0086 (-0.7σ) | +0.0075 (-4.6σ) | +0.0063 (-2.2σ) | 833.9 / 7 | 8.9e-176 | 3/7 | refuted |
| K2_loopsum | +0.0021 (-2.0σ) | +0.0021 (-0.4σ) | +0.0003 (+0.3σ) | +0.0121 (-9.3σ) | +0.0019 (+4.2σ) | +0.0003 (-1.2σ) | +0.0000 (+0.8σ) | 111.1 / 7 | 5.4e-21 | 4/7 | refuted |
| K3_modular | +0.0028 (-2.2σ) | +0.0028 (-0.6σ) | +0.0004 (+0.2σ) | +0.0105 (-29.5σ) | +0.0017 (+4.4σ) | +0.0003 (-1.2σ) | +0.0000 (+0.8σ) | 896.0 / 7 | 3.5e-189 | 4/7 | refuted |
| K3b_cosx | +0.0075 (-3.3σ) | +0.0075 (-1.7σ) | +0.0150 (-2.1σ) | +0.0113 (-28.2σ) | +0.0113 (-2.3σ) | +0.0113 (-6.1σ) | +0.0113 (-4.3σ) | 874.3 / 7 | 1.7e-184 | 1/7 | refuted |

The same, split by set (the split is not in PREDICTIONS.md):

| candidate | loop^2 >= 12 (T01, T12, N72): chi2 / dof, p | loop^2 = 9 (Q36, Q45, Q54, Q63): chi2 / dof, p |
|---|---|---|
| K1_l2 | 23.7 / 3, p 2.9e-05 | 1222.6 / 4, p 2e-263 |
| K1a_angle | 15.7 / 3, p 0.0013 | 818.2 / 4, p 8.6e-176 |
| K2_loopsum | 4.3 / 3, p 0.23 | 106.9 / 4, p 3.4e-22 |
| K3_modular | 5.2 / 3, p 0.16 | 890.8 / 4, p 1.7e-191 |
| K3b_cosx | 18.3 / 3, p 0.00038 | 856.0 / 4, p 5.7e-184 |

## Post hoc (after the data)

- **Refits.** Refitted on all ten pairs (P1–P3 pooled, the seven new ones), every candidate fails (χ² ≥ 300 on 8–9);
  refitted on the six pairs with loop² ≥ 12 only, K2 (χ² 8.4 on 4, p 0.08, K = 1.43) and K3 (9.9 on 5, p 0.08,
  κ = 10.0) are acceptable, K1, K1a, K3b are not (p ≤ 2 × 10⁻⁵). Their fitted parameters barely move from the forecast ones.
  `python3 research/shape3/explore3.py` (→ `data/explore.txt`).
- **Lattice-scale quantities next to the differences** (`data/explore.txt`, first table): transverse layer counts,
  cuts, rows and the near-firewall rate (checks with two adjacent dead transverse layers) do not order the pairs.
  The near-firewall rate is 12 times higher on the shorter-lived face of P1 but higher on the *longer*-lived face
  of P2 (review's runs: 1.49 against 1.21 per 10⁶ life-generations) and differs by 5% in Q36, where d is the
  largest. Rows: the shorter-lived face has the extra short row in Q36, Q45, P1 and P3, but not in Q54 (d ≈ 0 with
  rows {3, 6, 6} against {3, 18, 18}) and not in P2 (refuted in-sample).
- **Q36 is not an artefact of the zombie lives** that the first (stopped) run carried: the v1 value was −0.027
  (biased), −0.023 for young lives; the v2 value −0.0223 ± 0.0007 is flat in age (−0.022, −0.023, −0.022 in the
  bins 0–256, 256–1k, 1k–4k).


## Reproduce

    bash research/shape3/validate3.sh > research/scratch/shape3/validate.log 2>&1          # ~5 min
    python3 research/shape3/predict3.py --write                                            # forecasts (before the runs)
    nohup python3 research/shape3/run3.py lane 0 0-3 > research/scratch/shape3/lane0.log 2>&1 &
    nohup python3 research/shape3/run3.py lane 1 0-3 > research/scratch/shape3/lane1.log 2>&1 &
    python3 research/shape3/analyze3.py collect     # scratch event files -> data/runs.csv, data/agebins.csv
    python3 research/shape3/analyze3.py report      # every table above, from the two CSVs (-> data/report.txt)
    python3 research/shape3/explore3.py             # post hoc invariants table (-> data/explore.txt)

`data/runs.csv` holds the raw counts per job (exposure, F, X, W, S, open, near-firewall checks);
`data/agebins.csv` exposure and face deaths per job in age bins. Event files are in `research/scratch/shape3/`
(git-ignored).

## Not checked

- **The cap-free P2 rerun was not run** (budget: the machine was shared). So the review's question whether
  the P2 difference grows with the age of a life is still open; P1 shows no such growth.
- **Second stepper only for Q36, Q45, P1 and one (2,4,12) job** (REVIEW-shape3.md, see "Reviewed"). Q54, Q63,
  P3, N72 and the A = 72 triple were not rerun apart from that one job; the A = 72 nulls rest on ts3's counts
  (recounted from the raw event files) plus that job. ts3 is the review of shape2's ts.c with a faster kernel
  (validated bit-for-bit against the engine for 4,000 generations on every torus, and against ts.c's own event
  files) and a new settled test. The settled test is event logic, not stepping: it was checked by construction
  (exact equality proves periodicity), by the zombies vanishing, and by identity with ts.c when built with one lag;
  not against the engine. Periods p with p / gcd(p, 840) ≥ 129 are still not caught (none occurred among the
  review's 12,968 settled lives, largest period 52); no open life older than about 13.5 mean lives remained. The
  per-torus values agree with the earlier independent runs (above).
- Not recomputed by the review: the post hoc material (`explore3.py`), the age-bin tables (`data/agebins.csv`) and
  the age-dependence summary. Zombie rates at A ≥ 54 were not measured.
- Events are resolved every 8 generations, not per generation; ties are ≤ 0.4% of face deaths here and moving them
  changes no difference by more than 0.0005.
- The A = 72 precision (± 0.0041 to ± 0.0061) is short of the ± 0.003 asked: it excludes the size-free candidates
  (forecasts 0.007–0.015) but cannot tell K2 or K3 (≤ 0.003) from zero, nor K2 from K3 anywhere.
- Whether the loop² 9 sign change is a small-area effect (A = 36 is a 36-cell face) or a property of loop² 9: only
  four pairs, one per area. On Q54 and Q63 firewalls are 14% and 98% of face deaths (cut 108), so those faces live
  next to a strong competing channel.
- The candidate list is not exhaustive: anything that depends on the slab thickness (8 layers) or on the soup
  density was not considered; the soup is 0.4 everywhere.

