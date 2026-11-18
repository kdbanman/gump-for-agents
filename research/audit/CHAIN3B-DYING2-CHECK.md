# Check of the 120-cell tube, the CPU second code and the two dying studies (2026-11-18)

Rows and tables at main 3215b5e (the card's branch merged at 415dc66). Arithmetic and logic from committed rows and
tables only; nothing re-run, no death record opened (they are in `research/scratch`).

    python3 research/audit/gpu_chain3b_lead_check.py    # 0.6 s; part 1; ends PASS
    python3 research/audit/dying2_check.py              # 0.2 s; part 2; ends PASS

Estimator as `CHAIN3-CHECK.md`: ln τ_face = ln(2 ΣE / ΣF) over a face's seeds, error 1/√F, seeds' χ² from per-seed
values; a CPU seed is the sum of its chunks.

# Part 1: tubes and the CPU second code

## 1. The 120-cell tube (1, 18), (0, 40)

**24.5086 ± 0.0169**: 3,494 face deaths, 8 seeds of 180 min (24.0 GPU-hours), seeds' χ² 4.4 on 7 (per seed 24.465 to
24.580). No firewall, no settled life, no kind-5 life; 2,560 lives open at the end of each run. All equal the card's.
`hist_1_18_40.json` has the same exposure and face deaths as the rows, to the unit. The rows name three code commits
(e472355, 81681d7, 327e8dd); between them only `AGENT.md`, `README.md` and `USAGE.md` changed under `research/gpu-local`,
`research/gpu` and `research/shape`, so all eight ran the same code. `checks/check_1_18_40.txt` now holds the
GPU-against-engine lines (three kernels equal for 2,000 generations × 5 lanes, both negative controls differ), which
the previous check found missing.

## 2. The four long tubes of loop² 12 together

| cells | ln τ_face | deaths | seeds | χ² |
|---:|---:|---:|---:|---:|
| 84 | 17.3175 ± 0.0031 | 107,478 | 2 | 0.0 on 1 |
| 96 | 19.7446 ± 0.0042 | 56,775 | 8 | 10.0 on 7 |
| 108 | 22.1599 ± 0.0086 | 13,641 | 8 | 6.8 on 7 |
| 120 | 24.5086 ± 0.0169 | 3,494 | 8 | 4.4 on 7 |

- Chords 0.20227 ± 0.00043 (84 → 96), 0.20127 ± 0.00079 (96 → 108), **0.19572 ± 0.00158 (108 → 120)**.
- Second differences −0.0119 ± 0.0124 at 96 cells (−1.0σ), **−0.0666 ± 0.0244 at 108 (−2.7σ)**; third difference
  −0.055 ± 0.033 (−1.6σ).
- **The one line through 84 to 108 cells is excluded at 120 cells.** That line is 19.7419 + 0.20198 (A − 96), slope
  ± 0.00031, χ² 0.93 on 1. At 120 cells it gives 24.5893 ± 0.0097 (with the fit's covariance). The measured value is
  **0.0808 ± 0.0195 below it, 4.1 combined errors** (two-sided p 3.5 × 10⁻⁵). A single line through all four points
  has χ² 18.1 on 2 (p 1.2 × 10⁻⁴).
- Discount against 13.1623 + 0.20861 (A − 63): 0.2256, 0.3018, 0.3898, 0.5445.

**Smooth forms through all four points.** Each has one parameter more than a line and is linear in its parameters.
**These are fitted after seeing the 120-cell value.** They describe the four points and test nothing. "A slope that
falls like 1/length" and "a term in ln A" are the same form: slope s + k/A integrates to s A + k ln A, which is
τ ∝ A^k e^{sA}. The third form below lets the slope fall like 1/A², a 1/A term in ln τ.

| form | χ² on 1 (p) | residuals (σ) at 84, 96, 108, 120 | slope at 120 | 126 cells (1,19),(0,42) | 132 cells (1,20),(0,44) |
|---|---:|---|---:|---:|---:|
| constant curvature, c = (−9.9 ± 2.5) × 10⁻⁵ per cell² | 2.68 (0.10) | +0.15 −0.62 +1.26 −0.83 | 0.1966 | 25.699 ± 0.022 (± 0.037 inflated) | 26.868 ± 0.032 (± 0.053) |
| a + s A + k ln A, k = 1.88 ± 0.49, s∞ = 0.1816 ± 0.0052 | 3.34 (0.07) | +0.14 −0.63 +1.39 −0.99 | 0.1973 | 25.707 ± 0.021 (± 0.038) | 26.884 ± 0.029 (± 0.053) |
| a + s A + k/A, s∞ = 0.1912 ± 0.0027 | 3.66 (0.06) | +0.13 −0.63 +1.45 −1.06 | 0.1976 | 25.710 ± 0.020 (± 0.039) | 26.890 ± 0.028 (± 0.053) |
| for reference: the line through 84–108 | | | 0.2020 | 25.801 ± 0.012 | 27.013 ± 0.013 |
| for reference: a + sL − ln(1 + 2e^{−L/1.95}), L = A/12, K and ξ held at the theory session's values, a and s refitted (2 dof) | 11.46 on 2 | −0.70 +1.20 +1.00 −2.92 | 0.1999 | 25.760 ± 0.010 | 26.962 ± 0.012 |
| the card's block 9 (120-cell value + 0.196 per cell) | | | | 25.685 ± 0.035 | 26.855 ± 0.060 |

"Inflated" means multiplied by √χ². None of the three forms fits well (p 0.06 to 0.10). Each wants the 108-cell point
higher and the 120-cell point lower than it can give: the four points bend more sharply between 108 and 120 cells
than any smooth one-parameter bend allows. The three forms agree with one another at 126 and 132 cells within 0.011
and 0.022, less than their own errors. So the coming tubes cannot tell them apart. They can tell all three from the
84–108 line, which is 0.09 to 0.10 higher at 126 cells and 0.12 to 0.15 higher at 132, against expected measurement
errors of about ± 0.030 and ± 0.055 (block 9). The fixed-K = 2 form, refitted, already fails at 120 cells (−2.9σ).

## 3. Forecasts on file for the 120-cell tube

| forecast | value | measured − forecast | in errors |
|---|---:|---:|---:|
| the card, block 7 (frozen 2026-11-17T01:15Z, before any row) | 24.576 ± 0.020 | −0.0674 | −2.6 combined |
| theory session, PI block 0 | 24.56 ± 0.03 | −0.0514 | −1.5 |
| theory session, `tube1d` | 24.563 ± 0.030 | −0.0544 | −1.6 |
| theory session, `tube1d` later K = 2 fit | 24.571 | −0.0624 | −3.7 (measurement's error) |
| theory session, K = 1 case | 24.608 | −0.0994 | −5.9 (measurement's error) |
| theory session, `model` | 24.575 ± 0.025 | −0.0664 | −2.2 |
| theory session, `rigour` | 24.570 ± 0.025 | −0.0614 | −2.0 |
| theory session, `split-slab` bookkeeping | 24.59 ± 0.05 | −0.0814 | −1.5 |
| theory session, `split-slab` surrogate (referee's pool) | 24.60 ± 0.07 | −0.0914 | −1.3 |
| the 84–108 line (WL10, on file at 03:14Z; written as a 120-cell number only after the rows, in FROM-THE-LEAD 12:07Z) | 24.5893 ± 0.0097 | −0.0808 | −4.1 |
| the frozen 54–84 tube line (WL3) extended (never written for 120 cells) | 24.6841 ± 0.0093 | −0.1755 | −9.1 |

The theory session's numbers are from the "Forecasts frozen before the data" table of `research/blast/REPORT.md` on
`claude/exciting-hamilton-0h2tr1` at f7918ca, which is not merged. Its own note says the first five extrapolate the same
three anchors and are not independent. Every forecast is high. Measured in each forecast's own error, the block-7
forecast is the farthest off (2.6). The block-7 bet "within 0.04 of 24.576, 75%" failed. "Kind-5 lives: none, 85%"
held. Neither the notebook nor `FROM-THE-LEAD.md` holds a 120-cell forecast frozen by the lead.

## 4. The CPU second code (`research/data/gpu_local_cpu/`)

| face | layers | CPU (seeds, deaths, χ²) | GPU | CPU − GPU |
|---|---:|---|---:|---:|
| (1, 17), (0, 32), 96 cells | 8 | 19.7394 ± 0.0065 (12, 23,904; 9.1 on 11) | 19.7446 ± 0.0042 | −0.0052 ± 0.0077 (−0.7) |
| (1, 4), (0, 28), 84 cells | 8 | 17.5442 ± 0.0034 (8, 84,908; 9.1 on 7) | 17.5387 ± 0.0031 | +0.0055 ± 0.0046 (+1.2) |
| (1, 4), (0, 21), 63 cells | 8 | 13.1607 ± 0.0017 (8, 361,543; 10.6 on 7) | 13.1622 ± 0.0007 | −0.0016 ± 0.0018 (−0.9) |
| (1, 4), (0, 21), 63 cells | 16 | 13.1619 ± 0.0025 (4, 156,800; 4.1 on 3) | 13.1589 ± 0.0013 | +0.0030 ± 0.0029 (+1.1) |
| (4, 0), (0, 4), 48 cells | 8 | 9.9252 ± 0.0006 (3, 3,009,239; 1.5 on 2) | 9.9251 ± 0.0004 | +0.0002 ± 0.0007 (+0.3) |

The five differences together have χ² 3.8 on 5. The values quoted by the card (19.7394 ± 0.0065 with 23,904 deaths and
twelve seeds; 17.5442 ± 0.0034 with 84,908 deaths and eight seeds) recompute exactly. The 96-cell CPU run is partial:
its last chunk started at 11:35Z on the 18th and the run was to end about 19:30Z. Each file also keeps the 5-minute
seeds 9000–9003 (527 deaths at 84 cells).

**The loop-21 face (1, 4), (0, 28), pooled over the two codes: 17.5411 ± 0.0023.** That is +0.0071 ± 0.0046 (+1.5σ)
from 17.534 ± 0.004 (the density relation) and −0.0059 ± 0.0038 (−1.6σ) from 17.547 ± 0.003 (the effect ends before 21).
**It sits 0.0006 above their midpoint, 17.5405.** The GPU alone leaned to the relation (0.9 against 1.9); the CPU
alone leans the other way (1.9 against 0.6); pooled, it leans neither way. Below the wide-face line at 84 cells it is
−0.0030 ± 0.0023 (the line WL8 used, 17.5442) or −0.0020 ± 0.0023 (the line refitted with the 6 × 6, 17.5431), without
the line's own error. WL9's pair (the 6 × 6 and this face) changes from χ² 1.4 against the relation and 5.8 against
"long ways round cost nothing" (the notebook's 5.7, from rounded inputs) to **2.9 and 4.4 on 2**: neither is excluded,
and the preference has weakened.

**Which claims rest on two codes now:**
- **WL7 / WL10:** two codes at 84 cells (the lead's CPU face, and the GPU) and at 96 cells. At 96 the CPU now has 12
  seeds and agrees (−0.7σ); the CPU value alone is 4.7σ below the frozen tube line (it was 3.3). One code (the GPU) at
  108 and 120 cells, so **the 120-cell bend rests on one code and one lattice.**
- **WL8:** now on two codes. They agree (+1.2σ). The pooled value is at the midpoint, so the claim's "leans to a
  cost" should become "between the two, undecided".
- **CN4:** unchanged. Only the 63-cell value at 16 layers has a second code. The CPU's own thickness difference at 63
  cells is +0.0013 ± 0.0030 where the GPU's is −0.0033 ± 0.0015 (the two differ by 1.4σ). The 12-layer value, the
  84-cell 16-layer value and the 16-layer price 0.20863 are one code.

## Discrepancies in the card's part-1 write-up

- Block 9 writes 26.855 for the 132-cell forecast, which is 24.5086 + 12 × 0.1955. Its 126-cell 25.685 uses 0.196. On
  its stated basis (0.196 per cell) the 132-cell forecast is 26.861, a 0.006 difference, a tenth of its error.
- Nothing else in the 120-cell bullets or block 9 fails to recompute: the value, deaths, χ², chord, second difference,
  the line's 24.589 ± 0.010, the 0.081 ± 0.020 shortfall, the discount 0.545, the line's 25.801 and 27.013, and the
  CPU values.

# Part 2: the dying studies (`research/dying2/`, `research/dying2/hull/`)

## 5. What each measured, and the headline numbers

**Wrapped faces** (`research/dying2/README.md`, recorder `dy.c`, a copy of `fr.c`). It recorded face deaths, the dips
that recovered and the excursions below P̄ on four 8-layer slabs: W63 (1,4),(0,21); E84 (2,4),(0,14); T84 (1,12),(0,28);
T96 (1,17),(0,32). It holds 8,000, 2,500, 2,500 and 2,503 deaths (15,503 in all), with 31,723, 19,148, 19,628 and
33,434 recovered dips recorded.
- Every wrapped face holds its population until about 12 generations before death and empties in the last 4 to 6.
- The point of no return is 2.59 to 2.73 live cells on all four faces.
- The tube's discount at 84 cells is in how often it reaches a few cells (ν), not in q.
- Only on tubes does an empty band across the axis open while a third of the face is alive.
- Dying dips fall faster and their survivors are more spread than in dips that recover.
- The layer beneath falls to 0.55 to 0.64 of its stationary population.

**Recomputed from the CSVs, equal to the README to its last digit:** for each face q(1..5), k* and k*/P̄, ln ν(≤k) at
k = 2, 5, 10 and at 0.9, 0.7, 0.5 P̄, the tail slope, [ln ν(0.9) + ln τ]/A, P/P̄ at lags 1 to 16, live cells at lag 1,
the layer beneath at lags 4, 2, 0, X at lag 2 and its null, the band widths at lags 8, 4, 2, 1 with their nulls, the
final 1-edge cut's median lag, X at count k (dying, recovered, null), and the catches' q against the online q (equal
to within 5 × 10⁻⁶). Also recomputed: the W63 → E84 comparison (ln ν(≤2) −4.40, q(2) −0.008) and T84 − E84 at P̄/2
(ln ν +0.56, ln q −0.35). One rounding: T96's "P 4 generations before the catch at k = 4" is 46.55 against 43.22, a
difference of 3.3, written 46.6 and 3.4. Taken from the reports and not recomputed (they need the records): the plunge
medians, X at t_h, the 2-edge cut variant and the passage times.

**Hull faces** (`research/dying2/hull/README.md`, recorder `hd.c`). The vessel is the exact octahedral hull of
`facelaw.py`, soup 0.35, T0 = 200, at R = 11 (faces of 63 cells) and R = 13 (84 cells). It holds 42,494 and 8,891 face
deaths (4,500 and 8,705 dumped).
- q(k) is the same at both sizes for k ≤ 3 (0.769/0.770, 0.499/0.496, 0.298/0.296).
- k* is 2.00 and 1.98 cells.
- A death is a collapse of about 16 generations.
- Dying and recovering dips look alike on the way down.
- The last cells sit by the rim and next to the corners. Remnants on the rim and spread-out remnants die more often.

**Recomputed from the CSVs, equal to the README:** q at k = 1, 2, 3, 4, 6, 9 and their errors, k* and k*/P̄, ln ν(min ≤ 3),
the dead excursions (42,489 and 8,891), P/P̄ at lags 32 to 1, the lag-1 count (mean 1.62/1.61, 5% 1, median 1, 95% 4),
the neighbours at death, the row and corner shares at lag 1, the condq tables at k = 4 and 6 and the k = 3 spread split,
the equal-depth numbers at k = 3, ln τ 84 − 63 = 4.508, ln(q(9) ratio) = 0.133, and the q(6) difference (5.5σ). The
censored share at k ≤ 9 is ≤ 0.001.

## 6. The unreconciled q(k)

| | q(1) | q(2) | q(3) | recovery at |
|---|---:|---:|---:|---|
| W63 | 0.860 | 0.641 | 0.447 | P ≥ 33 (P̄ 32.58) |
| E84 / T84 / T96 | 0.853 / 0.846 / 0.855 | 0.633 / 0.623 / 0.625 | 0.422 / 0.413 / 0.422 | P ≥ 44 / 44 / 50 |
| hull R = 11 / R = 13 | 0.769 / 0.770 | 0.499 / 0.496 | 0.298 / 0.296 | P ≥ 32 / 43 (U = ⌈P̄⌉) |

At 63 cells, W63 minus the hull is +0.091, +0.142, +0.150 (23σ to 38σ) at k = 1, 2, 3.

**The formula and the bookkeeping are the same in the two codes** (`dy.c` `count_ring_tally`/`events`; `hd.c`
`events`; `dyan.py` and `analyze.py`):
- An excursion starts at the first generation below the threshold after one at or above it, both at age > T0. The
  threshold is in effect ⌈P̄⌉ in both: `dy.c` tests P ≥ P̄ with P̄ fractional, `hd.c` tests P ≥ U with U = ⌈P̄⌉.
- An excursion ends recovered at the first generation back at the threshold, and dead when the face is empty.
- A death enters at minimum 0, so it counts for every k. In both codes the empty generation is counted before the
  death is tallied; on the wrapped side this is shown by ν(≤k)·q(k) equalling the death rate to < 10⁻⁴.
- An excursion still open when the life ends for another reason is censored and left out of q.
- q(k) = dead / (dead + recovered with minimum ≤ k), cumulative in k, in both.

**They differ in which cells count, and in small things:**
1. **The cell set.** A hull face's 63 (84) cells include its rim row: 33 of 63 (39 of 84) cells, holding 0.51 (0.46)
   of a living face's live cells. That row is also counted in an edge neighbour's face (`hullvessel.py`: faces share
   cells; `nface` = 2 on the rim). So "k cells left" on a hull face can be cells that a living neighbour also owns. A
   recovery can then be the neighbour's population spilling back into the shared row, an event a wrapped face cannot
   have. A wrapped face's cells are its own; only the layer beneath and its own remnant can refill it.
2. T0 is 200 on the hull and 512 on the slab; the soup density is 0.35 and 0.4. Neither should matter if the faces are
   stationary by T0; not tested here.
3. A hull life ends when any of 8 faces dies, a slab life when either of 2 faces dies or a firewall closes. The
   censoring that follows is ≤ 0.001 at k ≤ 9 on the hull and zero at k ≤ 3 on the slab, so it does not explain the
   gap.

So the two numbers measure the same quantity on different cell sets. The 0.09 to 0.15 gap is not shown to be about
rims, or anything else, until the cell sets match.

**A like-for-like comparison would need**, from the hull's dumped face-layer states (1,024 generations per death and
per capped recovered dip, in scratch):
- q(≤k) recomputed with the count restricted to cells no other face owns (rows ≥ 1), or, equivalently for the
  question, q(≤k) restricted to remnants with no cell in the shared row. The hull's `condq` comes close, but it is q
  at the first passage to *exactly* k (its "all" row at k = 2 is 0.373, against q(≤2) = 0.499), so it cannot be set
  beside the wrapped q(≤k) as it stands.
- The same estimator for the wrapped faces: q at the first passage to exactly k, which the wrapped records allow and
  `_catches.csv` does not tabulate.
- Recovery reweighted for the capped recovered dumps, as `condq.py` does.
- Ideally T0 = 512 on the hull.

The cleanest pair is W63 against R = 11 (both 63 cells).

## 7. The dying face by lag before death

The quantiles are as tabulated. The wrapped tables give q75 and q90 at lags 1, 2, 3, 4, 6, 8, 12 (no lag 5, 7, 9, 10,
11). The hull tables give q75 and q95 at lags 1 to 6, 8, 10, 12 (no 7, 9, 11). The "living" reference is the same
table's rows at lags ≥ 64 (wrapped) or ≥ 32 (hull), averaged: dying faces far from their death.

As fractions of the living mean P̄ (in brackets, as fractions of the face, P/A):

| face (P̄/A; living median, q75, upper q) | lag 1 | lag 2 | lag 3 | lag 4 | lag 6 | lag 8 | lag 12 |
|---|---|---|---|---|---|---|---|
| **W63** (0.517; 1.013, 1.105, q90 1.197) mean | 0.052 | 0.131 | 0.323 | 0.567 | 0.776 | 0.894 | 0.977 |
| median / q75 / **q90** | 0.031 / 0.061 / 0.092 | 0.092 / 0.153 / 0.276 | 0.184 / 0.368 / 0.862 | 0.338 / 1.044 / **1.442 [0.746]** | 0.921 / 1.074 / **1.350 [0.698]** | 0.982 / 1.105 / 1.228 | 1.013 / 1.105 / 1.197 |
| **E84** (0.518; 1.009, 1.087, q90 1.160) mean | 0.038 | 0.094 | 0.229 | 0.448 | 0.719 | 0.860 | 0.969 |
| median / q75 / **q90** | 0.023 / 0.046 / 0.069 | 0.069 / 0.115 / 0.207 | 0.115 / 0.276 / 0.437 | 0.230 / 0.506 / **1.426 [0.738]** | 0.874 / 1.058 / **1.380 [0.714]** | 0.966 / 1.081 / 1.242 | 0.989 / 1.104 / 1.173 |
| **T84** (0.515; 1.003, 1.086, q90 1.168) mean | 0.038 | 0.090 | 0.210 | 0.421 | 0.697 | 0.845 | 0.966 |
| median / q75 / **q90** | 0.023 / 0.046 / 0.069 | 0.069 / 0.115 / 0.185 | 0.115 / 0.254 / 0.416 | 0.208 / 0.485 / **1.432 [0.738]** | 0.808 / 1.039 / **1.386 [0.714]** | 0.970 / 1.086 / 1.247 | 0.993 / 1.086 / 1.178 |
| **T96** (0.515; 1.008, 1.088, q90 1.160) mean | 0.034 | 0.080 | 0.181 | 0.372 | 0.645 | 0.824 | 0.961 |
| median / q75 / **q90** | 0.020 / 0.040 / 0.061 | 0.061 / 0.101 / 0.162 | 0.101 / 0.222 / 0.384 | 0.182 / 0.424 / **1.395 [0.719]** | 0.566 / 1.031 / **1.354 [0.698]** | 0.950 / 1.071 / 1.233 | 0.990 / 1.091 / 1.172 |

| hull face (P̄/A; living median, q75, q95) | lag 1 | lag 2 | lag 3 | lag 4 | lag 5 | lag 6 | lag 8 | lag 10 | lag 12 |
|---|---|---|---|---|---|---|---|---|---|
| **R = 11** (0.496; 1.002, 1.120, q95 1.267) mean | 0.052 | 0.114 | 0.206 | 0.314 | 0.412 | 0.506 | 0.676 | 0.801 | 0.874 |
| median / q75 / **q95** | 0.032 / 0.064 / 0.128 | 0.096 / 0.160 / 0.288 | 0.160 / 0.256 / 0.544 | 0.224 / 0.416 / 0.928 | 0.320 / 0.576 / 1.088 | 0.416 / 0.768 / 1.152 | 0.704 / 0.960 / 1.216 | 0.864 / 1.024 / 1.248 | 0.928 / 1.056 / 1.248 |
| **R = 13** (0.505; 1.013, 1.100, q95 1.225) mean | 0.038 | 0.081 | 0.148 | 0.233 | 0.329 | 0.423 | 0.611 | 0.752 | 0.851 |
| median / q75 / **q95** | 0.024 / 0.047 / 0.094 | 0.071 / 0.094 / 0.212 | 0.094 / 0.188 / 0.419 | 0.165 / 0.306 / 0.660 | 0.236 / 0.448 / 0.989 | 0.330 / 0.613 / 1.084 | 0.589 / 0.919 / 1.201 | 0.825 / 1.013 / 1.201 | 0.919 / 1.060 / 1.225 |

The fractions of the face are the P̄ fractions times P̄/A (0.515 to 0.518 wrapped, 0.496 and 0.505 hull);
`dying2_check.py` part D prints both for every entry.

**Plainly:**
- **A dying wrapped face passes through a generation far fuller than a living face usually is, about four generations
  before it dies.** On all four faces the 90% quantile at lag 4 is 1.40 to 1.44 P̄. That is 0.72 to 0.75 of the
  face's cells (47, 62, 62, 69 cells), 2.9 to 3.3 σ_P above P̄, and 0.23 to 0.27 P̄ above the living face's own 90%
  quantile (1.16 to 1.20 P̄). At lag 6 it is still 1.35 to 1.39 P̄; by lag 3 it is 0.38 to 0.86 P̄.
- At lag 4 the distribution is split: the median is 0.18 to 0.34 P̄, q75 is 0.42 to 1.04, q90 is 1.40 to 1.44. At
  least 10% (and, from q75, at most 25%) of dying faces are then above 1.40 P̄, and the rest have already fallen.
  **The mean never exceeds P̄ at any lag**, so the over-full generation shows only in the upper quantiles.
- **A dying hull face does not, as far as the tables reach.** Its 95% quantile rises steadily towards the living q95
  from lag 1 to 12 (0.13 → 1.25 P̄ at R = 11, 0.09 → 1.23 at R = 13) and never exceeds it (largest 39 cells against a
  living 39.6; 52 against 52.0). At lag 4 it is 0.93 and 0.66 P̄. Fewer than 5% of dying hull faces are above 0.93 P̄
  at lag 4 and above 1.15 P̄ at lag 6. The hull's mean and median also fall earlier and more gradually: the median is
  0.59 to 0.70 P̄ at lag 8, against 0.95 to 0.98 on the wrapped faces.
- **What the tables cannot say.**
  - "Far fuller than a living face *ever* is" cannot be checked: the stationary P histogram is not in `data/`. The
    living face's 90% quantile is 1.16 to 1.20 P̄. A Gaussian with the measured σ_P would put about 0.1% of living
    generations above 1.40 P̄, an assumption only.
  - A hull over-fill in fewer than 5% of deaths would not show in q95.
  - The wrapped and hull tables give different upper quantiles (q90 against q95) and skip different lags (lag 5 is
    not tabulated for the wrapped faces).
  - A like-for-like test would take the share of deaths whose face exceeds, say, 1.3 P̄ within the last 8 generations,
    from the records on both sides.

## 8. Validation, and what does not follow

**How each stepper was validated (as reported; not re-run).**
- **Wrapped (`dy.c`).** Its step is `fr.c`'s, compared with the engine every generation for 2,000 generations on all
  four tori (3 engine soups × 3 lanes), with two negative controls. Its records and tallies were compared with an
  independent numpy stepper on (1,4),(0,10) × 8 (30,000 generations, with deaths) and on (1,17),(0,32) × 8 (6,000
  generations, no death), on lanes 0–127; the README reports both IDENTICAL. **No validation log is kept in `data/`.**
  End to end, its four ln τ sit −1.7, +0.6, +1.6 and −1.4σ from the card's GPU values (the README's −1.2 for T96 was
  against the four-seed 19.7405).
- **Hull (`hd.c`).** Its step was compared with `gump run --cells` for 3,000 generations on 5 lanes per size, and its
  face counter with numpy on all 256 lanes; both negative controls differ. `data/validate.log` holds both "VALIDATE OK"
  lines. Each dump is checked as it is read. Its two ln τ sit +1.4 and +0.9σ from the GPU's. Both studies' forecasts
  were committed before any table (a47fa31, b851756) and have not been edited since.

**What in the READMEs does not follow from the data:**
1. *Wrapped: "censored; none occurred".* The excursion tables hold 4,004, 1,198, 1,249 and 1,254 censored excursions
   (W63, E84, T84, T96). They are about half the deaths: the other face's open excursion when a face dies. Their
   smallest minimum is 4 on W63 and 17 to 22 on the others, so q(k ≤ 3) is untouched. The "ν·q identity, nothing
   censored" remark holds to 8 × 10⁻⁵ for that reason, not because nothing was censored.
2. *Wrapped: "q(k) agrees across the four faces within 0.01–0.03 at every k ≤ 5" and "k\* is the same on every
   face".* The spread at k = 3 is 0.034. W63 is above E84 by 0.025, 0.027 and 0.023 at k = 3, 4, 5 (3.4σ, 5.0σ, 6.0σ,
   binomial). The three faces of 84 and 96 cells agree within 0.009 at every k ≤ 5. The claim holds for them, and for
   all four only at k ≤ 2.
3. *Wrapped: "At ≤ 10 cells T84's dip rate is higher by 0.30 in ln ν with q equal".* At k = 10, ln q(T84/E84) is
   −0.093 ± 0.028 (3.3σ) and ln ν is +0.30. "q equal" holds at k ≤ 5 (|ln q| ≤ 0.022, within 1σ), where ln ν is
   +0.22 to +0.23, the whole lifetime gap (0.209). So the sentence is right at k ≤ 5 and wrong at k = 10.
4. *Wrapped: "every face death in these runs was [at age > 512]".* W63's report has 8,015 face deaths and 8,000 at
   age > 512; the 15 are not accounted for. This is minor.
5. *Plunge, across the two studies.* The hull's "plunge, last P ≥ P̄/2 to empty" (medians 7 and 8) is one generation
   longer by definition than the wrapped study's and round 1's t_d − t_h (t_h is the first generation below). On the
   wrapped definition the hull medians are 6 and 7 (means 6.47, 7.44), against 4 to 5 (means 5.03 to 5.90) wrapped.
   The dying2 README's comparison with round 1's c1 (6) is like for like; setting the hull study's 7 beside the
   wrapped 4 is not.
6. *Hull: "the rim row holds 1.10–1.14 of its stationary share".* The tables give 1.10 and 1.12 at lag 1, and 1.12 and
   1.16 at the first passage to 3 cells. This is minor.
7. *Hull: the edge neighbours' 19–23% loss at death* is largely the dying face's own empty rim row, which the
   neighbour also counts. The README says so ("which is the dying face's own"), but the loss should not be read as an
   effect on the neighbour's interior.
8. *Hull: the closing conjecture* ("if their q(k) matches these to the same 0.005, the two prices are all in ν").
   The wrapped q(k) does not match: it is 0.09 to 0.15 higher. Until the cell sets are made comparable (part 6), that
   does not show the prices differ in q either.
9. *Data defect.* `hull/data/R{11,13}_positions.csv` has unquoted commas inside its first field (`dying, lag 1`), so a
   CSV reader shifts every column. `dying2_check.py` rejoins the fields.

## Not checked

- Nothing was re-run: not the GPU or CPU runs, not their engine checks, not the dying recorders or their numpy
  checks. The validations above are as reported. Only the hull's `validate.log` is on file.
- The CPU code `fr.c` itself and its validation, which the lead has not reviewed. Whether the partial 96-cell CPU rows
  are final.
- The hazard by age in `hist_1_18_40.json` beyond its totals. The card's "flat over five bins, 0.94 to 1.06" was not
  recomputed.
- The theory session's forecasts were read from an unmerged branch (f7918ca) and taken as written. The fixed-K = 2
  refit assumes L = A/12 lattice units, as the card's block 9 states, and ξ = 1.95 from that report.
- Every death record and dump, which are in scratch. So: the plunge medians, X at t_h, the 2-edge cut, passage times,
  the hull figure, and the condq reweighting are taken from the studies' reports, not recomputed. The lag tables
  themselves (built by `dyan.py` and `analyze.py` from the records) are trusted as files. The code that builds them was
  read: the face layer is taken from the record's first column and the lag is counted back from the first empty
  generation.
- The smooth forms were fitted after the data and are not evidence for any of them. No form with more than one extra
  parameter was tried.
