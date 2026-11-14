# The second variable: equal area, equal shortest loop, different lifetime

2026-11-14. research/shape2 found that two periodic slab faces with the same area A and the same shortest loop can
differ in ln τ_face (by 0.015 at A = 48 and 0.014 at A = 60, the one with the shorter second loop dying sooner).
This experiment asks what the second variable is: five candidate formulas, each fitted on the three known pairs
only, forecast every new equal-area, equal-loop pair (`PREDICTIONS.md`, committed in 46baf66 before any production
run; amendments f645b13, 43a5e0e, ffcaf36, also before the results they concern). Statements are marked [proved],
[measured] or [conjectured]; "post hoc" means looked for after the data.

## Verdict

- **[measured] At A = 72 the equal-loop differences vanish.** The three new differences with shortest loop² ≥ 12
  are T01 = −0.0044 ± 0.0046, T12 = +0.0016 ± 0.0045 and N72 = +0.0018 ± 0.0061, all zero within 1σ, where the same
  kind of pair differs by +0.015 at A = 48 (re-measured here cap-free: +0.0144 ± 0.0019) and by +0.014 at A = 60.
  The shape term between *different* shortest loops grows with area (+0.06 at 60, +0.10 at 72, research/shape2);
  the term at *equal* shortest loop does not.
- **[measured] Below saturation (shortest loop² 9) the differences are large and change sign.** Q36 (A = 36):
  **−0.0223 ± 0.0007**, the face with the *longer* second loop dying sooner, 30σ; Q45 (A = 45): +0.0076 ± 0.0013;
  Q54 (A = 54): −0.0020 ± 0.0019. No candidate forecast a negative difference anywhere.
- **Candidates** (forecast parameters fitted on the three known pairs only, `PREDICTIONS.md`; scored on six new
  differences; Q63 was not run):

  | candidate | committed score (6 differences) | loop² ≥ 12 alone (3) | loop² 9 alone (3) | verdict |
  |---|---|---|---|---|
  | K1 second loop, linear | χ² 1225, p 10⁻²⁶¹ | 17.0, p 7 × 10⁻⁴ | 1208 | **refuted**, in both sets |
  | K1a angle, linear | 824, p 10⁻¹⁷⁴ | 10.3, p 0.016 | 813 | **refuted** (by the loop² 9 set; at loop² ≥ 12 alone p 0.016) |
  | K3b cos 2π Re τ, size-free | 850, p 10⁻¹⁸⁰ | 12.8, p 0.005 | 838 | **refuted**, in both sets |
  | K2 loop sum Σ e^{−1.41 \|v\|}, amplitude ∝ A | 108, p 5 × 10⁻²¹ | **2.1, p 0.55** | 106 | refuted by the committed rule (Q36 −9σ, Q45 +4σ); **survives out of sample at loop² ≥ 12** |
  | K3 modular e^{−2πh} cos 2π Re τ | 893, p 10⁻¹⁸⁹ | **2.6, p 0.45** | 890 | refuted by the committed rule (Q36 −30σ, Q45 +4σ); **survives out of sample at loop² ≥ 12** |
  | firewall cut, short rows, layer count, number of shortest loops, "shorter third loop dies sooner" | — | — | — | refuted in-sample, before the runs |

  What survives at loop² ≥ 12 is the statement both K2 and K3 make: **the equal-loop effect decays as the torus gets
  longer in its second direction (larger h = Im τ)** and is ≤ 0.003 at A = 72. The test does not separate K2 from K3
  (they forecast within 0.001 of each other everywhere tested), nor either from "zero at A = 72". Their survival
  is a forecast of "nearly nothing" that came true, which is weaker than a forecast of a size; the size-free forms
  (K1, K1a, K3b), which forecast 0.007–0.015 at A = 72, are what the test excludes. Below saturation both fail.
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
are few: at A ≤ 84 they occur only at A = 48, 60, 72 and 84 (none at 54, 63, 66 or 75), two pairs and one triple
at 72. Below saturation, Q1 = 9 groups exist at A = 36, 45, 54, 63, 72.

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
  7 × 10⁶ against a mean life of 800, carrying 1.7% of the exposure. Earlier work never saw this because its caps
  (6.5 × 10⁴, 5 × 10⁵) censored them. ts3 compares the state with snapshots 840·m generations back in the same
  life, m = 1 … 128, and censors at the first match. Exact equality proves periodicity, so no chaotic life is cut.
  After the change, no torus has an open life older than about 12 mean lives (`data/runs.csv`, column `open`; the
  oldest ages were checked from the event files).
- **Plan** (`run3.py list`): seeds 31001–31062, fixed before the runs. Wall time is the only stopping rule. The
  machine was shared with other jobs and gave each of the two lanes 20–60% of a core, so the plan was cut short:
  see "What was run".

## What was run

All of plan v2's jobs before the A = 72 rounds (one job per torus at A = 36, 45, 48, 54 and for P3), and A = 72
rounds 1–4 of the triple and both rounds of N72 (rounds 5 of the triple still running when this was written). Not run: Q63 and the cap-free rerun of P2 (both
queued after the A = 72 rounds; the machine was shared, the lanes got 20–75% of a core). 12 A = 72 jobs of
7.5 × 10⁷ generations × 512 replicas. Per-job counts: `data/runs.csv`.

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
| (1,8,20) | 60 | 1 | 2.304e+10 | 186,263 | 19 | 13 | 512 | 12.4187 ± 0.0023 | 12.4187 | 123,322 |
| (2,2,10) | 60 | 1 | 2.304e+10 | 184,871 | 0 | 0 | 512 | 12.4262 ± 0.0023 | 12.4262 | 124,263 |
| (1,5,24) | 72 | 4 | 1.536e+11 | 96,596 | 5,151 | 43 | 2048 | 14.9725 ± 0.0032 | 14.9720 | 1,479,227 |
| (1,6,24) | 72 | 4 | 1.536e+11 | 96,325 | 5,122 | 36 | 2048 | 14.9753 ± 0.0032 | 14.9749 | 1,483,585 |
| (1,10,24) | 72 | 2 | 7.680e+10 | 53,171 | 0 | 0 | 1024 | 14.8763 ± 0.0043 | 14.8763 | 1,417,053 |
| (2,2,12) | 72 | 2 | 7.680e+10 | 53,269 | 0 | 0 | 1024 | 14.8745 ± 0.0043 | 14.8745 | 1,414,521 |
| (2,4,12) | 72 | 4 | 1.536e+11 | 96,746 | 5,098 | 38 | 2048 | 14.9709 ± 0.0032 | 14.9705 | 1,477,904 |

Agreement with earlier, independent data (different seeds and codes, all capped): (2,2,8) 9.9260 ± 0.0013 here,
9.9254 ± 0.0015 in the review of shape2, 9.9243 ± 0.0020 in shape2; (1,6,16) 9.9404 / 9.9410 / 9.9384;
(1,8,20) 12.4187 ± 0.0023 / 12.4220 / 12.4148; (2,2,10) 12.4262 / 12.4270 / 12.4223; at A = 72 research/shape's
single runs (± 0.014) gave 14.984 (1,6,24), 14.968 and 14.974 (two presentations of (2,4,12)), 14.965 (1,5,24),
14.875 (2,2,12), 14.878 (1,10,24). So the cap (≥ 4 mean lives in those runs) did not bias these values at the level
of their errors.

Firewalls (W), ties (X, face death and firewall at the same 8-generation check) and settled lives (S) are
≤ 0.4% of face deaths on every loop² ≥ 12 torus and on Q36; on Q45 and Q54 (cut 108) firewalls are 2% and 14% of
face deaths, identical within pairs. Counting ties as face deaths moves no difference by more than 0.0005, so the
8-generation check window does not bias the pairs compared (and both members of a pair have the same window).

## Pair differences [measured]

d = ln τ_face(Y) − ln τ_face(X), Y the class with the longer second loop; error √(1/F_X + 1/F_Y). "young" and
"old": lives younger / older than 65,536 generations (A ≤ 60; about 0.5–6 mean lives) or 1,048,576 (A = 72, about
0.7 mean lives).

| pair | X -> Y | d | ties as face | young (< 65,536; A = 72: < 1,048,576) | old |
|---|---|---|---|---|---|
| P1 | (2, 2, 8) → (1, 6, 16) | **+0.0144 ± 0.0019** | +0.0149 | +0.0143 ± 0.0019 | +0.0634 ± 0.0462 |
| P3 | (1, 8, 20) → (2, 2, 10) | **+0.0075 ± 0.0033** | +0.0076 | +0.0102 ± 0.0051 | +0.0056 ± 0.0043 |
| T01 | (1, 6, 24) → (2, 4, 12) | **-0.0044 ± 0.0046** | -0.0044 | -0.0066 ± 0.0064 | -0.0020 ± 0.0065 |
| T12 | (2, 4, 12) → (1, 5, 24) | **+0.0016 ± 0.0045** | +0.0015 | +0.0131 ± 0.0064 | -0.0104 ± 0.0065 |
| T02 | (1, 6, 24) → (1, 5, 24) | **-0.0028 ± 0.0046** | -0.0029 | +0.0065 ± 0.0064 | -0.0124 ± 0.0065 |
| N72 | (2, 2, 12) → (1, 10, 24) | **+0.0018 ± 0.0061** | +0.0018 | +0.0041 ± 0.0085 | -0.0007 ± 0.0089 |
| Q36 | (1, 4, 12) → (1, 3, 12) | **-0.0223 ± 0.0007** | -0.0225 | -0.0223 ± 0.0007 | — |
| Q45 | (1, 5, 15) → (1, 4, 15) | **+0.0076 ± 0.0013** | +0.0078 | +0.0076 ± 0.0013 | — |
| Q54 | (3, 0, 6) → (1, 5, 18) | **-0.0020 ± 0.0019** | -0.0020 | -0.0015 ± 0.0021 | -0.0067 ± 0.0062 |

P1 and P3 are the known pairs, re-measured cap-free (in-sample for every candidate). Pooled with the earlier values
(research/audit/REVIEW-shape2.md): **P1 +0.0148 ± 0.0013, P3 +0.0069 ± 0.0024** (2.9σ; it was 1.8σ). The age
dependence the review hinted at (difference growing with age, 2σ, on P2) is not seen in P1: by age bin +0.016 ±
0.007, +0.018 ± 0.004, +0.012 ± 0.003, +0.015 ± 0.004 for ages 256–1k, 1k–4k, 4k–16k, 16k–65k (the mean life is
10⁴). P2 itself was not rerun. All age bins: `analyze3.py report`, last block.

## Forecasts scored

Committed rule: z = (measured − forecast)/√(σ_m² + σ_f²), hit if |z| < 2; refuted if Σz² over the new differences
has p < 0.01.

| candidate | T01 | T12 | N72 | Q36 | Q45 | Q54 | chi2 / dof | p | hits | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| K1_l2 | +0.0051 (-2.1σ) | +0.0152 (-2.9σ) | +0.0152 (-2.1σ) | +0.0051 (-34.5σ) | +0.0101 (-1.6σ) | +0.0051 (-3.5σ) | 1224.9 / 6 | 1.9e-261 | 1/6 | refuted |
| K1a_angle | +0.0075 (-2.6σ) | +0.0070 (-1.2σ) | +0.0111 (-1.5σ) | +0.0111 (-28.1σ) | +0.0086 (-0.7σ) | +0.0075 (-4.6σ) | 823.6 / 6 | 1.2e-174 | 3/6 | refuted |
| K2_loopsum | +0.0021 (-1.4σ) | +0.0021 (-0.1σ) | +0.0003 (+0.3σ) | +0.0121 (-9.3σ) | +0.0019 (+4.2σ) | +0.0003 (-1.2σ) | 108.3 / 6 | 4.7e-21 | 4/6 | refuted |
| K3_modular | +0.0028 (-1.6σ) | +0.0028 (-0.3σ) | +0.0004 (+0.2σ) | +0.0105 (-29.5σ) | +0.0017 (+4.4σ) | +0.0003 (-1.2σ) | 892.7 / 6 | 1.4e-189 | 4/6 | refuted |
| K3b_cosx | +0.0075 (-2.6σ) | +0.0075 (-1.3σ) | +0.0150 (-2.1σ) | +0.0113 (-28.2σ) | +0.0113 (-2.3σ) | +0.0113 (-6.1σ) | 850.4 / 6 | 2e-180 | 1/6 | refuted |

The same, split by set (the split is not in PREDICTIONS.md):

| candidate | loop^2 >= 12 (T01, T12, N72): chi2 / dof, p | loop^2 = 9 (Q36, Q45, Q54, Q63): chi2 / dof, p |
|---|---|---|
| K1_l2 | 17.0 / 3, p 0.0007 | 1207.9 / 3, p 1.4e-261 |
| K1a_angle | 10.3 / 3, p 0.016 | 813.3 / 3, p 5.8e-176 |
| K2_loopsum | 2.1 / 3, p 0.55 | 106.2 / 3, p 7.2e-23 |
| K3_modular | 2.6 / 3, p 0.45 | 890.1 / 3, p 1.2e-192 |
| K3b_cosx | 12.8 / 3, p 0.0051 | 837.6 / 3, p 3e-181 |

## Post hoc (after the data)

- **Refits.** Refitted on all nine pairs (P1–P3 pooled, the six new ones), every candidate fails (χ² ≥ 316 on 7–8);
  refitted on the six pairs with loop² ≥ 12 only, K2 (χ² 6.2 on 4, p 0.18, K = 1.39) and K3 (7.3 on 5, p 0.20,
  κ = 10.0) fit, K1, K1a, K3b do not (p ≤ 2 × 10⁻⁴). Their fitted parameters barely move from the forecast ones.
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

- **Q63 and the cap-free P2 rerun were not run** (budget: the machine was shared). So the review's question whether
  the P2 difference grows with the age of a life is still open; P1 shows no such growth.
- **No second stepper for these numbers.** ts3 is the review's ts.c with a faster kernel (validated bit-for-bit
  against the engine for 4,000 generations on every torus, and against ts.c's own event files) and a new settled
  test. The settled test is event logic, not stepping: it was checked by construction (exact equality proves
  periodicity), by the zombies vanishing, and by identity with ts.c when built with one lag; not against the engine.
  Periods p with p / gcd(p, 840) ≥ 129 are still not caught; no open life older than about 12 mean lives remained.
  The per-torus values agree with the earlier independent runs (above).
- Events are resolved every 8 generations, not per generation; ties are ≤ 0.4% of face deaths here and moving them
  changes no difference by more than 0.0005.
- The A = 72 precision (± 0.0045 to ± 0.006) is short of the ± 0.003 asked: it excludes the size-free candidates
  (forecasts 0.007–0.015) but cannot tell K2 or K3 (≤ 0.003) from zero, nor K2 from K3 anywhere.
- Whether the loop² 9 sign change is a small-area effect (A = 36 is a 36-cell face) or a property of loop² 9: only
  three pairs, one per area.
- The candidate list is not exhaustive: anything that depends on the slab thickness (8 layers) or on the soup
  density was not considered; the soup is 0.4 everywhere.

