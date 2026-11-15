# Review of the GTX 1080 session's equilateral face tori (branch `claude/gpu-local-1080`, 34cd2d3..b843883)

Adversarial review, 2026-11-15. Object: what the session on the owner's GTX 1080 added after the part reviewed in
`research/audit/REVIEW-gpu-local-pr23.md` (which covered up to 34cd2d3):

- `research/gpu-local/README.md`, "The torus driver, calibrated on 4 × 4" and "Equilateral face tori": five
  equilateral face tori (8 {111} layers, soup 0.4, ln τ_face = ln(2E/F)) from one GPU driver, `eqtorus.py`;
- the claim that the tori of 63, 75 and 93 cells lie on one line of slope 0.2084 and that the bend is all below 63;
- the claim that research/shape2's CPU census (`research/peeling/rep.c` through `research/shape/tslab.py`) is biased
  by its 16-generation stamping, +0.0016 at A = 48 (`research/gpu-local/cpu4x4/`);
- the forecasts of `research/gpu-local/PREDICTIONS.md` blocks 2 and 3, and the bookkeeping of the rows
  `research/data/gpu_local_eqtorus/eqtorus_*.csv`.

There is no GPU here. The review measured the 57-cell and 75-cell tori with a stepper of its own, checked against
`reference/oracle.py` every generation. It ran rep.c on the same lives at both resolutions, refitted the five values,
and read the branch's source and commit history. Code and small outputs are in `research/audit/gpu_local_tori/`;
bulk output is in `research/scratch/audit_gpu_local_tori/` (not in git). Commands run from the repository root, with
`D=research/audit/gpu_local_tori S=research/scratch/audit_gpu_local_tori`. `WT` is a checkout of b843883
(`git worktree add research/scratch/wt-gpu-local-tori b843883`). The branch was fetched once, at the start, at b843883.

## Verdicts

| # | claim (the card's number) | verdict | this review |
|---|---|---|---|
| 1 | A = 57, (1,7),(0,19): 11.8756 ± 0.0006; seeds 11.8742, 11.8771 (2.6σ apart) | **confirmed** | **11.8744 ± 0.0015** (own stepper, 445,165 face deaths, 4 seeds χ² 0.71 on 3). −0.0012 ± 0.0016 from the card. It is 0.1σ from seed 57001 and 1.7σ below seed 57002: it leans to the lower seed but excludes neither. |
| 2 | A = 75, 5 × 5: 15.6630 ± 0.0023 | **confirmed** | **15.667 ± 0.010** (own stepper, 9,646 face deaths, 2 seeds χ² 0.54 on 1). +0.004 ± 0.010 from the card, +0.006 from the file's 15.6614. |
| 3 | A = 48, 63, 93 | not re-measured | 48 and 63 have independent values already (9.9246 ± 0.0006, `REVIEW-gpu-local-pr23.md`; 13.176 ± 0.011, `REVIEW-dying.md` Round 3 claim 8). **93 still has one code.** |
| 4 | one line through 63, 75, 93, slope 0.2084 | **confirmed** (arithmetic) | c = 0.20840 ± 0.00014, χ² 0.0002 on 1. Deficits: −0.111 at 48, −0.036 at 57. |
| 5 | "the bend is all below A = 63"; the deficit "is gone by a shortest loop of about 4.6" | **consistent, not established; and the shape is not a decay** | The test has one degree of freedom. At 2σ it allows a slope change of 0.0009 above 63, or a residual of 0.01 at 63. **No smooth correction decaying in the loop or in 1/A fits the five (χ² 68–117 on 1).** Only a line kinked near A = 61.4 fits (χ² 0.000). |
| 6 | rep.c's 16-generation rule reads ln τ high: +0.0016 at A = 48 | **confirmed** | **+0.00167 ± 0.00006** on the file's own 311,296 lives (rep.c at K = 16 and K = 1, same lives). |
| 7 | "it scales like 16 generations over the mean life … negligible from A ≈ 60 up" | **refuted as stated** | At A = 60: +0.0184 ± 0.0011 for the systole² 4 class (1,9,20), +0.00076 for (1,1,20), +0.0003 for (1,4,20). At A = 48, (2,0,8): +0.0174. Ties with firewalls carry most of it, not the 16 generations of exposure. |
| 8 | blocks 2 and 3 committed before the rows they forecast | **confirmed, on commit times** | Block 2 was committed at 05:46:55Z, and the first A = 57 run started at 05:49:04Z. Block 3 was committed at 06:13:51Z, when no file for 81–111 existed. These are client clock times; no server push time was available. |
| 9 | settled lives censored correctly in ln(2E/F) | **confirmed** | They stay in E, to recognition, and out of F. Their exposure past settling is under 10⁻⁶ of E. Own A = 57: 2.6 × 10⁻⁴ cycles per face death (card 2.56 × 10⁻⁴), all of period ≤ 10. |
| 10 | launch caps "3% or less of the mean life" | **confirmed** (63 is 3.2%) | 2.9%, 3.2%, 2.1% and 0.25% of E/lives at 57, 63, 75 and 93. At 48 it is 20%, which the README itself warns about. |
| 11 | `code_commit` | **mislabelled, harmless here** | The commit is HEAD at the *end* of a run, with no dirty-tree mark. The stepping code did not change from 95fc5bf to b843883. The 4 × 4 row still says ea43aaf. |
| 12 | the five must-fix items of `REVIEW-gpu-local-pr23.md` | **none closed** | Item 1 is done except the pointer to the review. Items 2–5 are not done. |

## 1. The 57-cell torus, measured here (and the 75-cell one)

**Stepper** (`tor.c`, `geo.py`). Nothing is imported from `research/`. `geo.py` builds the slab from AUTOMATON.md:
- every +ax face of the cubes (i, j, k) with t = i + j + k in [0, 8), with (i, j) reduced modulo the lattice;
- the 12 doubled offsets of section 2, and a neighbour is dead if its cube has t outside [0, 8);
- the transverse layer index s_d = d·p mod P_d, with P_d = gcd of d·(2g) over the lattice generators.

It checks for every lattice in part C:
- neighbours are distinct and symmetric;
- every interior cell has 12 neighbours with T1's layer histogram;
- s_d is consistent along every edge.

The result: (1,7),(0,19), (1,4),(0,21), (1,5),(0,31) and (1,10),(0,37) have P = 4 on all three diagonals. That
is two transverse layers, so no firewall can form, as the card says. (5,0),(0,5) has 10 layers, (3,3),(0,9) has 6,
(2,4),(0,14) has 4 and (6,0),(0,6) has 12.

`tor.c` is bit-sliced with 512 lanes. Every lane holds one life at a time and reseeds the moment it ends, from a hash
of (seed, lane, life, cell). Every generation it checks, in this order:
- a firewall: three cyclically consecutive dead transverse layers, on diagonals with ≥ 3 layers;
- a face death: layer t = 0 or 7 empty. A firewall in the same generation wins, as on the card.
- a cycle: a return to the lane's snapshot, taken at ages 1, 2, 4, …, so any period is caught.

E is the sum of ages at the end of every life, open lives included.

**Validation.**

    gcc -O3 -march=native -o $S/tor $D/tor.c
    python3 $D/geo.py 1 7 19 $S/g_1_7_19.bin; python3 $D/geo.py 5 0 5 $S/g_5_0_5.bin
    python3 $D/val.py 1 7 19 19 3000 2      # -> val_1_7_19_out.txt
    python3 $D/val.py 5 0 5 15 3000 2       # -> val_5_0_5_out.txt
    python3 $D/replay.py 4 0 4 1 3000000 777 40; python3 $D/replay.py 1 7 19 1 2000000 778 30   # -> replay_out.txt

- `val.py` tiles the slab into the oracle's H = 2N array-index torus. For 57 cells, N = 19: N Z² lies in the lattice,
  and 11 dead layers separate the copies, which T3 keeps dead. For 75 cells, N = 15.
- It steps `reference/oracle.py` and requires, at every generation, that the oracle state is lattice-periodic and
  reduces to exactly tor's node set. Two soups × 3,001 generations each: **0 mismatches on both tori.**
- Three negative controls each fail on both tori:
  - tor's generation g against the oracle's g + 1: 300 of 300 generations mismatch;
  - a mutant rule with survival also at n = 6: 300 of 301;
  - one rewired edge: 296 and 293 of 301.
- `replay.py` regenerates the soups of sampled lives from (seed, lane, life). It steps them with a separate numpy
  rule and applies the event rules written out again.
  - On 4 × 4 (which has firewalls) it replayed all 49 firewall lives, all 4 cycles, 40 face deaths and 40 open
    lives.
  - On 57 cells it replayed 30 face deaths and 30 open lives.
  - Every kind, age and snapshot age matches (`replay_out.txt`).

**A = 57 result** (`ana57_out.txt`):

    for s in 5701 5702 5703 5704; do $S/tor run $S/g_1_7_19.bin 8 $s 15600000 $S/p57_s$s.rec; done   # ~6 min each, 1 core
    python3 $D/ana.py $S/p57_s570?.rec

| | this review | card |
|---|---:|---:|
| face deaths | 445,165 | 3,283,133 |
| ln τ_face | **11.8744 ± 0.0015** | 11.8756 ± 0.0006 |
| per seed | 11.8733, 11.8736, 11.8740, 11.8765 (χ² 0.71 on 3) | 11.8742, 11.8771 (χ² 6.9 on 1) |
| cycles per face death | 2.63 × 10⁻⁴ (117; periods 1: 87, 2: 12, 3: 8, 4: 6, 5: 2, 6: 1, 10: 1) | 2.56 × 10⁻⁴ (settled12 + settled3pw = 840) |
| hazard, ages 0–60 / mean | 1.69 ± 0.07 | "1.6 to 2.0" |
| hazard beyond 2 / 4 mean lives / mean | 0.999 ± 0.004 / 1.007 ± 0.011 | |

- The card's pooled value stands (Δ = −0.0012 ± 0.0016). This value sides with the card's lower seed: Δ = +0.0002
  from 57001 and −0.0027 ± 0.0017 from 57002.
- The 2.6σ split between the card's two seeds is therefore most likely a fluctuation in 57002, but a value at
  ± 0.0015 cannot settle that.
- No cycle here had a period above 10. None would have needed the guard on the card.
- The hazard is flat from age 60 to 4 mean lives within 0.3–1%. That excludes unrecognised long cycles at the level
  that matters.
- The 57-cell torus is one where stepper, soups and conventions are all independent of the card's. Their
  agreement to 0.0012 also checks the GPU driver's counting on a torus without a firewall channel.

**A = 75 result**

    for s in 7501 7502; do $S/tor run $S/g_5_0_5.bin 8 $s 30000000 $S/p75_s$s.rec; done   # ~21 min each, 1 core
    python3 $D/ana.py $S/p75_s750?.rec        # -> ana75_out.txt

- 9,646 face deaths and 22 firewalls in 3.07 × 10¹⁰ life-generations. **ln τ_face = 15.6670 ± 0.0102**; the seeds
  give 15.6745 and 15.6596 (χ² 0.54 on 1).
- The card has 15.6630 ± 0.0023 (Δ = +0.004 ± 0.010) and the file 15.6614 ± 0.0026.
- ln τ_fw = 21.06 ± 0.21, against the card's 20.94: E/(fw + fw_settled) = 5.83 × 10¹¹ / 470.
- No cycle of any period was found, and the hazard is flat within errors from age 3,000 to 2.4 × 10⁷.
- The 75-cell value is confirmed at ± 0.010. That is enough to exclude an error of the size of the deficits, not to
  test its fourth decimal.

## 2. The 16-generation rule of rep.c

**What rep.c records** (`research/peeling/rep.c`, read whole):
- Every generation, each layer's OR over its cells goes into an accumulator.
- At generations divisible by K the accumulator is stamped: `la[L] = gen` for every layer that had a live cell since
  the last stamp. A final flush stamps the last generation.
- `lc2`, the last change against t − 2, is stamped the same way. A periodic state is detected by comparison at
  multiples of 840.

`tslab.run` calls it with K = 16. `death_times` gives D = la + 1, so a death is booked at the next multiple of 16
plus 1: 0–15 generations late, 7.5 on average. A layer whose last stamp equals the final generation counts as never
dead.

`tslab.stats` takes the first of face, firewall and stop. Ties go to the firewall, and a death tied with the
settle time or the cap is censored. So K = 16 does two things:
- it lengthens every event-ended life by 7.5 generations on average (the exposure part);
- it moves face deaths into "firewall", "settled" or "cap" when they share a 16-generation window with one of those
  (the count part).

**Measurement on the same lives.** rep.c is deterministic in (graph, W, p, seed, cap). K changes only the stamping,
so a job run at K = 16 and at K = 1 holds identical lives. `bias.py` calls the repository's own `tslab.tslab` and
`Vessel.run` with each K and reduces each output exactly as `tslab.run` and `tslab.stats` do. Every K = 16 job is
**bit-identical** to research/shape2's own per-job file in `research/scratch/shape2/` (`repro.py`; 196 of 196
jobs).

    python3 $D/bias.py run 4 0 4 16384 1008000 76     # the file's 76 jobs (~12 min); likewise:
    python3 $D/bias.py run 2 0 8 8192 1002000 40; python3 $D/bias.py run 1 9 20 8192 2002000 40
    python3 $D/bias.py run 1 1 20 32768 2001000 20; python3 $D/bias.py run 1 4 20 65536 2009000 20
    for c in "4 0 4" "2 0 8" "1 1 20" "1 9 20" "1 4 20"; do python3 $D/bias.py stats $c; python3 $D/repro.py $c; done   # -> bias_out.txt

| A | class (systole²) | jobs (seeds as drive2.py) | mean life | ln(2E/F), K = 16 | K = 1 | bias | exposure part | count part |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 48 | (4,0,4) (16), the file's whole row | 76/76 | 10,265 | 9.93237 | 9.93070 | **+0.00167 ± 0.00006** | +0.00073 | +0.00094 |
| 48 | (2,0,8) (4) | 40/80 | 2,280 | 9.48308 | 9.46571 | **+0.0174 ± 0.0005** | +0.0033 | +0.0141 |
| 60 | (1,1,20) (3) | 20/30 | 11,250 | 10.02123 | 10.02048 | +0.00076 ± 0.00003 | +0.00067 | +0.00009 |
| 60 | (1,9,20) (4) | 40/168 | 2,584 | 11.17761 | 11.15922 | **+0.0184 ± 0.0011** | +0.0029 | +0.0155 |
| 60 | (1,4,20) (16) | 20/50 | 131,347 | 12.48373 | 12.48346 | +0.0003 ± 0.0001 | +0.00006 | +0.00022 |

(The error on the bias is the spread of the per-job differences, which is far below the statistical error of
either value, since the lives are the same. Mean life here is E/(F + W).)

**4 × 4.**
- The cross-table matches the card's `xtab.py` in kind. 247,338 face deaths at K = 16 are all face deaths at K = 1.
- Of the 247,570 per-generation face deaths, K = 16 books 110 as firewalls, 20 as settled and 102 as capped.
- The pr23 review's emulation of the grid on its own renewed lives gave only +0.0008 (its section 2 table). That
  matches the exposure part. It missed the count part, because renewed lives with no cap and exact firewall times
  have no ties to lose.
- So the earlier statement "no systematic cause exists" for the file's 9.9324 should read: +0.0017 from the rule,
  and the rest a draw.
- On the K = 1 basis the file reads 9.9307 ± 0.0020, against the pooled 9.9249 ± 0.0003: +0.0058, or 2.9σ (the
  earlier review said 3.4σ with the error scaled).
- The pr23 review's "fresh rep.c" value, 9.9240 ± 0.0014, is a K = 16 number. On the per-generation basis it is
  about 9.9223. Pooled with the GPU's value and t4's, the best value barely moves, to about 9.9248.

**What it does to values on file.**
- *Long-lived classes* (systole² ≥ 7 at A = 60, mean lives ≥ 10⁵): ≤ 0.0003, negligible against their ± 0.003.
- *The A = 48 classes with mean lives near 10⁴*, and (1,1,20) at A = 60: +0.0008 to +0.0017, about 0.4–0.8σ of a
  ± 0.002 row.
- *Systole² 4 classes at every area* — (2,0,8), (1,7,16) at 48; (1,9,20), (2,0,10) at 60: +0.017 to +0.018. That
  is several times their stated errors.
  - This part was found before: `REVIEW-shape2.md` claim 1 estimated "about 0.018 at A = 48" from 2,048 lives. The
    shape2 README flags those rows.
  - New here: the same size at A = 60, measured on 164k lives.
- **Differences between classes at one area.**
  - A systole² 4 class against any long-lived class moves by about −0.016 at 48 and −0.018 at 60.
  - Between classes of similar mean life (systole² 7–16 at 48), the difference moves by the difference of their
    biases. The only one measured at 48 is 4 × 4, at +0.0017. (1,1,20) at 60 has a similar mean life and no
    firewall channel, and gives +0.0008. So those classes probably carry +0.0008 to +0.0017, and their differences
    move by under 0.001, against ± 0.003 for a difference. This was not measured class by class.
  - (1,1,16) at 48 (systole² 3, mean life 2,700) was not measured. Its exposure part alone is about +0.003.
  - Among the long-lived classes at 60, differences move by under 0.001.
  - The cost per cell b, a difference across areas within one class, is nearly immune: (4,0,4) +0.0017 at 48, and
    the 60-cell long classes ≤ 0.0003 (shape2 README).

**The card's text.** "Scales like 16 generations over the mean life" describes the exposure part only (7.5/10,265 =
0.0007). The count part depends on the firewall channel, the cap and the settling rate:
- (1,1,20) has a mean life like 4 × 4's and a bias half as large (no firewall channel, a longer cap);
- systole² 4 classes are ruled by ties.

"Negligible from A ≈ 60 up" is false for the systole² 4 rows at 60, and probably at 72 (6.9% of face deaths tie
there, per `REVIEW-shape2.md`). It is true for the long-lived classes.

## 3. The line, and what else fits the five

    python3 $D/line.py        # -> line_out.txt

The five values as recomputed from the rows: 48: 9.9251 ± 0.0004, 57: 11.8756 ± 0.0006, 63: 13.1622 ± 0.0007,
75: 15.6630 ± 0.0023, 93: 19.4141 ± 0.0053. Every lattice was checked to be equilateral (6 shortest vectors of
norm² n). The shortest loop is l = √(A/3).

**The line through 63, 75, 93.** c = 0.20840 ± 0.00014, a = 0.0331, χ² = 0.0002 on 1.
- The two local slopes agree to 10⁻⁵, against an error of 4.4 × 10⁻⁴. P(χ² ≤ 0.0002) = 1%, an unusually good
  agreement but not by itself a sign of error.
- Deficits below the line: **−0.1111 at 48 and −0.0362 at 57.** With this review's 57 value, −0.0374; with the
  pooled 4 × 4, −0.1113.
- A side note: the README's table of "ln τ − 0.2088·A" uses 0.2088, not the fitted 0.2084. Its residuals
  (+0.008, +0.003, −0.004 at 63, 75, 93) are an artefact of that choice. At 0.2084 they are 0.000.

**How much the data say about "straight from 63".** One degree of freedom tests it. The difference of the two slopes
is −0.00001 ± 0.00044. At 2σ the data allow:
- a change of slope of 0.0009 between 69 and 84;
- or a residual of up to about 0.01 at 63 alone, if 75 and 93 lie on the line.

So "the deficit is gone by a loop of 4.6" means "below about 0.01 at 63 cells".

**Forms that try to fit all five** (4 parameters, 1 dof; the nonlinear parameter profiled on a grid, then refined):

| form | χ² on 1 | fits? |
|---|---:|---|
| E: a + cA − g e^{−(l−4)/λ} (constant price + correction decaying in the loop) | 116 | no |
| P: a + cA − g (48/A)^q (correction in 1/A) | 117 | no |
| M: a + A[c − g e^{−l/ξ}] (massive-like, per cell) | 113 | no |
| Q: a + cA + g₁/A + g₂/A² | 114 | no |
| S: a + cA − g e^{−(A/A₀)⁶} (decay much faster than exponential) | 15.3 | no (p ≈ 10⁻⁴) |
| H: a + cA − g (A₀ − A)₊² | 52.8 | no |
| **B: a + cA − g (A₀ − A)₊ (broken line)** | **0.000** | **yes**: kink at A₀ = 61.35 ± 0.15, slope 0.2167 below, 0.2084 above |

With A = 57's error inflated by √6.9 (its seeds' χ²), E, P, M and Q still give 59–70, and S gives 9.9.

**Why nothing smooth fits.** The deficit falls by a factor of 3.1 from 48 to 57, over ΔA = 9. It then has to fall
from 0.036 to below 0.01 within the next ΔA = 6, and to ~0 by 75. So its logarithm must fall faster and faster.
Any correction of the form g·f(A) with f exponential, power-law or quadratic-hinge does the opposite.

The five tori are described, to within their errors, by **two straight lines meeting near A = 61**. That is not a
finite-size correction fading out. Either something changes abruptly between loops √19 and √21, or one of 57 and 63
is off by about 0.01–0.03 for a lattice-specific reason. (Here they are the two tori with no firewall channel and
the shortest oblique loops.)

The independent values at 57 (this review) and 63 (CPU, 13.176 ± 0.011) exclude an error of the GPU driver as the
cause at 57, and above 0.03 at 63. **The README's conjecture of "a finite-size deficit that is gone by a shortest
loop of about 4.6" should say that the data need an abrupt change, not a decay.**

**Predictions for the four tori now running,** committed in `research/audit/gpu_local_tori/predictions.txt` at
**720ee7e** (06:27:41Z). The branch had not been fetched since b843883, which held no row for these tori. Errors are
statistical only. Tori of equal area and different lattice have differed by about 0.015 elsewhere.

| form | 81 (3,3),(0,9) | 84 (2,4),(0,14) | 108 (6,0),(0,6) | 111 (1,10),(0,37) |
|---|---:|---:|---:|---:|
| L / B: line from 63 (broken line) | 16.913 ± 0.002 | 17.539 ± 0.003 | 22.540 ± 0.006 | 23.165 ± 0.006 |
| C: L + free curvature κ(A−63)(A−93) | 16.913 ± 0.003 | 17.539 ± 0.003 | 22.540 ± 0.016 | 23.165 ± 0.019 |
| S: stretched (fails, χ² 15) | 16.914 ± 0.009 | 17.537 ± 0.011 | 22.515 ± 0.029 | 23.137 ± 0.032 |
| E: loop (fails) | 16.927 ± 0.023 | 17.547 ± 0.028 | 22.461 ± 0.154 | 23.070 ± 0.181 |
| P: 1/A (fails) | 16.927 ± 0.023 | 17.548 ± 0.028 | 22.458 ± 0.152 | 23.066 ± 0.179 |
| M: massive-like (fails) | 16.927 ± 0.023 | 17.547 ± 0.027 | 22.461 ± 0.144 | 23.071 ± 0.168 |
| Q: 1/A, 1/A² (fails) | 16.927 ± 0.023 | 17.547 ± 0.028 | 22.452 ± 0.132 | 23.060 ± 0.152 |
| card, block 3 | 16.913 ± 0.006 | 17.539 ± 0.007 | 22.540 ± 0.014 | 23.165 ± 0.015 |

- The card's errors are larger than the line's own statistical ones, because it takes the slope as ± 0.0003. That is
  close to form C's, which lets the curvature float.
- The sharpest test is A = 81. There the line and every smooth form differ by 0.014, against a planned ± 0.003.
- The line is refuted if 81 or 84 misses it by more than 3 combined σ, or if 108 and 111 both lie more than 0.03 off
  it on the same side.

## 4. Order and bookkeeping

**Forecast order** (`git log --format='%h %cI' 34cd2d3..b843883`; `start_utc` in the rows):

| block | commit | committed (UTC) | rows it forecasts | first `start_utc` |
|---|---|---|---|---|
| 2 (57, 63, 75) | 7d9956f | 05:46:55 | 57, 63, 75 | 05:49:04 (57), 05:56:28 (63), 06:04:21 (75) |
| 3 (81, 84, 108, 111) | 6b2dc2b | 06:13:51 | 81, 84, 108, 111 | not visible here (no row at b843883) |

- `git ls-tree 6b2dc2b research/data/gpu_local_eqtorus/` holds only the 48 and 93 files. So when block 3 was
  committed no 81–111 row existed, and the 57, 63 and 75 rows it quotes were not yet committed either; they came in
  b843883 at 06:14:26.
- Block 3 says the first A = 81 run "started a minute ago". The driver logs progress only every 300 s, so no partial
  count could have been seen. This rests on the session's word and on client-set commit times.
- `gh api repos/…/events` returned no push events for the branch, so no server-side time was available. Block 2
  states that it was written after the A = 93 result, which it was (39f165f, 05:45:15).

**Censoring of settled lives** (`eqtorus.run`, read):
- A life the kernel ends as kind 2 (period 1–2, recognised at c + 2) or kind 3 (period 3–128, recognised at the next
  launch start) is appended with age G + tt − birth. It is in E and not in F. That is correct: the time at risk
  before settling counts, and no face can die after it.
- Exposure carried past settling: at most 2 generations per kind 2 life, and at most one launch + P per kind 3 life.
  At 57 cells that is 104 × 2,048 / 2.36 × 10¹¹ < 10⁻⁶; at 63, 33 × 8,192 / 4.7 × 10¹¹ < 10⁻⁶.
- Kind 5 (guard) is zero in every row, so the two exposure conventions of must-fix item 2 coincide in these rows.
- This review's own run at 57 cuts a cycle at its first return to the snapshot. The exposure after the snapshot
  totals 185 generations (6 × 10⁻⁹ of E). Its cycle rate matches the card's (2.63 vs 2.56 × 10⁻⁴ per face death).
- Open lives at the end (2,560 per run) are censored at their ages, which is correct for this estimator.

**Launch caps against mean lives** (E / lives from the rows): 48: 2,048 / 10,200 = 20%; 57: 2,048 / 71,700 = 2.9%;
63: 8,192 / 259,000 = 3.2%; 75: 65,536 / 3.08 × 10⁶ = 2.1%; 93: 262,144 / 1.05 × 10⁸ = 0.25%.
- On tori without a firewall channel, the cap matters only through kind 3 latency, which is negligible (above).
- On 75 cells, a firewall forming mid-launch keeps its life running to the boundary. That overstates the exposure by
  at most 470 × 65,536 / 5.8 × 10¹¹ = 5 × 10⁻⁵.

**`code_commit`.**
- `eqtorus.py` writes `git_head()` after `run()` returns, so the field is HEAD at the end of the run, with no dirty
  marker. For example, the A = 93 runs started at 04:40:20Z and carry 34cd2d3, committed at 04:41:01Z.
- `git diff --stat 95fc5bf b843883 -- research/gpu research/shape research/gpu-local/eqtorus.py` is empty. So every
  row from 57 to 93 ran the stepping and counting code of 95fc5bf, and the numbers stand.
- The 4 × 4 row still says ea43aaf (must-fix 3).

**README text that claims more than its tables.**
- "Negligible from A ≈ 60 up" (the rep.c bias): false for systole² 4 classes (section 2).
- "Resolved: the file's value is high (a draw of its 76 seeds, plus a rule bias…)": right, and now quantified, as
  +0.0017 rule plus +0.0058 draw.
- "The bend is all below A = 63" and "a finite-size deficit that is gone by a shortest loop of about 4.6" rest on
  one degree of freedom (section 3). The second is tagged as a conjecture; the first is not, and should be.
- The "ln τ − 0.2088·A" column (section 3).
- "Lives older than 8 mean lives: … expected for memoryless lives". The expectation N·e⁻⁸ ignores censoring by the
  run's end. It is not checkable without the per-run json in any case.
- "Each torus passed `eqtorus.py check A K B` first": no output of these checks is committed for 57, 63 or 75.
- Block 2, "launch caps … 3% or less": 63 is 3.2% (trivial).

## 5. The must-fix list of `REVIEW-gpu-local-pr23.md`, at b843883

| item | state |
|---|---|
| 1. README: replace "not resolved" on 4 × 4, point to the review | **partly**: rewritten as "Resolved", but `REVIEW-gpu-local-pr23` is cited nowhere on the branch |
| 2. README: correct the latency conjecture; default to the snapshot-age cut of kind-5 exposure or report both | **not done**: the README's "both delays are small against a mean life" stands unchanged; the tori tables do not say that kind 5 = 0 makes the two conventions coincide |
| 3. 4 × 4 `code_commit`; `git_head()` to mark a dirty tree | **not done** (still ea43aaf; `git_head` unchanged) |
| 4. README: cite `REVIEW-gpu-pr14.md` for the settled-firewall undercount, bound its reach | **not done** |
| 5. PREDICTIONS: new block on the hull forecast's centre and the false "0 settled at A ≥ 90" premise | **not done** (blocks 2 and 3 do not mention it) |

## Must fix

1. README: the five items above; none is closed.
2. README, rep.c bias: replace "scales like 16 generations over the mean life … negligible from A ≈ 60 up" with the
   measured table (section 2):
   - the exposure part is 7.5/mean life;
   - the count part depends on ties with firewalls, the cap and settling;
   - +0.017 to +0.018 for systole² 4 classes at 48 and 60, ≤ 0.0003 for long-lived classes at 60.
   Cite `REVIEW-shape2.md` claim 1 for the systole² 4 part.
3. README, the line: tag "the bend is all below A = 63" as resting on one degree of freedom (2σ room: 0.01 at 63).
   Say that no smooth decaying correction fits the five and that only a kink near A ≈ 61 does. Replace the
   0.2088 column with residuals from the fitted 0.2084.
4. README, A = 57: add this review's 11.8744 ± 0.0015 as the second code. The seed split then looks like a
   fluctuation of seed 57002. Add more seeds if the fourth decimal matters.
5. `eqtorus.py`: record `git_head()` (with a dirty marker) at the start of a run, not the end.
6. Commit the `eqtorus.py check` output for each torus (57, 63, 75, and the four now running). Commit the per-run
   hazard tables (`hist`) in a small file: they are a few kB, and without them the hazard and old-life claims cannot
   be checked.

For the lead (not the card's to fix): the pr23 review's section 2 statement that no systematic cause exists for
the file's 4 × 4 value should be amended. The rule gives +0.0017 of the 0.0075, and the rest is a 2.9σ draw.
CLAIMS entries that use systole² 4 rows at A = 60 carry +0.018.

## Not checked

- Anything on the GPU: kernels, the `eqtorus.py check` runs, guard behaviour on these tori, throughput.
- Per-run files that exist only on the card's machine (`research/scratch/gpu-local/eqtorus_*.json`): the hazard by
  age, raw lives, the "older than 8 mean lives" counts, the kind breakdown of firewalled-and-settled lives. The
  +0.0016 of the 2¹⁸ calibration run is uncommitted too.
- A = 63 and 93 were not re-measured; A = 93 still has no second code.
- The card's 1,024 fresh rep.c jobs and 304 adjacent jobs (`cpu4x4/results_*.txt`). This review re-measured the
  bias on the file's own 76 jobs instead.
- Server-side push times. The forecast order rests on commit times set by the card's clock.
- Whether the 81 run had started when block 3 was written, and anything about the 81–111 rows. The branch was not
  fetched after b843883, by design.
- The rep.c bias at A = 72, and for the remaining A = 48 and 60 classes; they were inferred from the measured ones.
