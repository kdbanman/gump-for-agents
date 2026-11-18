# blast/toy — do gump's two exits exist in its 2D relative? (agent `toy`, 2026-11-18)

Rule: cross2 B34/S234 ("alive next iff n + x ≥ 3, except n ≥ 5 dies"; `research/toy2d/`). The "face" is an edge
row of L cells. **Ring** = edge row of a strip 16 × L periodic along the edge (the analogue of a wrapped face);
**box** = edge of an L × L box (the analogue of a hull face: two ends at corners). Tags: [proved] (by enumeration
or exact linear algebra), [measured] (one code unless said; error = 1/√deaths or binomial), [conjectured].
Commands run from this directory; bulk output in `research/scratch/blast/toy/`; curated output in `data/`
(`data/tables.txt` = `python3 table.py`, `data/anat.txt` = `python3 anat.py`). Forecasts: `PREDICTIONS.md`
(block 1 frozen before any run: 3 hits, 4 misses; block 2 frozen before the last exact runs and unscored data).

## Verdict

**Yes, both exits exist in 2D, and the rim does what it does in gump; but the prices are the other way round,
and that turns "two prices" into a crossover.** A ring edge dies by boom and bust (it over-fills to 85–90% of
the row against 57% alive, the cap kills it to 1–2 cells, they starve; no tilt), a box edge fades over 6–8
generations with its last cells at the corners. The ring's deaths split cleanly into a flash exit with
ln τ = 0.30 + **0.455**·L and a no-flash exit with ln τ = 4.03 + **0.327**·L; the box edge's no-flash exit has the
same price (0.31–0.34) and is e^0.73 ≈ 2 times faster; its flash exit is 3–5 times slower than the ring's. Because
in 2D the flash is the DEARER exit per cell (in gump it is the cheaper one), the ring's bust share falls like a
logistic in L (0.90 at 12 cells, 0.47 at 32; logit slope −0.128 ± 0.003 per cell; half at L = 29), its local price
falls from 0.44 to 0.40 towards the box's 0.34, and the measured "0.416 against 0.343" is a mixture, not two
asymptotic prices. The exactly solved one-row surrogate shows the same thing with no chaos beneath: ring and
open-segment prices are still 0.527 and 0.459 at L = 20 (not converging: a rim of two points changes the price at
every size I can reach), while the exact flash share of the ring falls with the same logit slope (−0.11 to −0.15
per cell). So: a rim does not set a price; it closes (taxes) the flash exit and opens ends for the fade, and the
observed price of a shape is the price of whichever exit carries its deaths at that size.

## 0. Codes and validation

- `ed.c`: one replica, one machine word per row, bit-sliced neighbour count; ring strips and boxes; books edge
  deaths with the last 16 generations of the dying row, living windows, the row-population histogram and its
  one-step transition matrix. Protocol as `research/toy2d/law.py`: soup p = 0.4, states younger than 300 not
  measured, a residence ends at an edge death, a 3-row interior firewall or a 3-column cut (strips), or a settled
  state (equal to a snapshot taken every 64 / 4096 generations). τ_edge = n_edges·exposure/deaths.
- `python3 validate.py` → **ALL OK**: state for state against a plain numpy stepper on toy2d's neighbour table,
  1000 generations, strips 16 × 20 and 5 × 64, boxes 18 and 11; against `toy2d/t2d.c` (population every generation
  and final state, 300 generations, same four vessels); negative control (neighbour (2,0) replaced by (3,0)) fails
  in 59 of 59 generations. A first version of `ed.c` detected only period ≤ 2 and stalled in oscillators (42 deaths
  in 6×10⁸ generations at L = 12); the snapshot test fixed it.
- `ex1d.c` (exact surrogate, cross2 row over coins) and `exg.c` (any range, coins, threshold, cap): in-place
  site-by-site kernel, h computed as the flux into the empty row. `ex1d 12 1 0.472` → 6.4169049205 and
  `ex1d 16 1 0.472` → 8.6349890757: the lab's 6.4169 and 8.6350 (`research/theory/exponent/exact1d.c`, an
  independent code). `exg L ring 2 2 3 4 0.472` reproduces `ex1d` to all printed digits (ring 12, segment 11).
  Segments have no second code [not checked beyond exg = ex1d, which share the kernel routine's design].

## 1. Neighbours inside the vessel [proved by enumeration: `python3 counts.py`]

| edge-row cell | in the row | beneath | total | can it be overcrowded (n ≥ 5)? |
|---|---|---|---|---|
| ring, any cell | 4 | 2 | 6 | yes |
| box, ≥ 2 from the corner | 4 | 2 | 6 | yes |
| box, next to the corner | 3 | 2 | 5 | only if every neighbour it has is alive |
| box, corner | 2 | 2 | 4 | **never** |

The 2D rim is 4 cells of L (gump's is a line of ~3k cells of 3k(k+1)/2). A corner cell with ≥ 2 live neighbours
always survives. In the surrogate segment the same holds for the end cell (2 in-row + 2 coins).

## 2. How they die [measured; `sh run_bf.sh` (8 min, one core), `python3 anat.py` → `data/anat.txt`, `data/anat.json`]

Deaths: 6000, 6000, 6000, 4000, 2000, 600 per geometry at L = 12 … 32. bustK = share of deaths whose last K
steps (fatal step included) contain a one-generation fall of the row population of at least L/2; "living" = the
same for living windows of K transitions (25,000–56,000 windows; 6,000–16,000 at L = 32).

| L | ring bust6 | ring bust12 | ring living12 | box bust6 | box bust12 | box living12 |
|---|---|---|---|---|---|---|
| 12 | 0.903 ± 0.004 | 0.931 | 0.36 | 0.490 ± 0.006 | 0.583 | 0.20 |
| 16 | 0.848 ± 0.005 | 0.876 | 0.21 | 0.384 ± 0.006 | 0.472 | 0.12 |
| 20 | 0.762 ± 0.005 | 0.802 | 0.12 | 0.314 ± 0.006 | 0.403 | 0.063 |
| 24 | 0.655 ± 0.008 | 0.703 | 0.063 | 0.237 ± 0.007 | 0.314 | 0.036 |
| 28 | 0.536 ± 0.011 | 0.586 | 0.034 | 0.172 ± 0.008 | 0.238 | 0.021 |
| 32 | 0.465 ± 0.020 | 0.513 | 0.017 | 0.152 ± 0.015 | 0.203 | 0.012 |

- **Ring = boom and bust.** Two generations before the empty row the population is bimodal: 10/50/90% =
  2/5/23 of 24 (2/6/19 of 20; 1/5/28 of 32) against 9/14/18 alive; one generation before: 1/2/3. The largest fall
  in the last 12 steps is 15 cells (median, L = 24; living windows 7) from a peak of 19.4 (living peaks 17.8; mean
  population 13.85), two to three steps before the end. Flat: the spread of last-alive times over the cells of
  one death is 1.1–2.1 generations, and the last living cells are uniform along the ring (0.165 within 2 of an
  arbitrary point against 0.167).
- **Box = a fade from the middle to the corners.** The population falls steadily over the last 8 generations
  (L = 24: 11.8, 11.2, 10.5, 9.5, 8.7, 8.2, 6.1, 1.8 against 14.2 alive), the largest fall is 9 (living 6) from a
  peak BELOW the living one (15.9 against 17.9: no boom), spread 2.3–3.1 generations, and the last living cells
  are within 2 of a corner 0.57, 0.45, 0.37, 0.33, 0.29, 0.27 of the time at L = 12 … 32 (uniform: 0.33 … 0.125):
  twice uniform at every size; the corner cell itself is last alive 0.6 generations later than the rest.
- The contrast is 2–3 in bust share, not gump's 40 (0.6 against 0.016), and both shares FALL with L (gump's
  wrapped share is flat or rising, 0.57 … 0.67). §3 says why.

## 3. Prices [measured; `python3 table.py` → `data/tables.txt`]

ln τ_edge, mine pooled with `research/toy2d/data/law_cross2_B34S234{,_box_none}.json` (what was on file: the
ring law to L = 36 and the box to L = 32, read there as "0.416" and "0.343"; what I added: 2–5 times the deaths at
L ≤ 28, the per-edge comparison, the anatomy and the split):

| L | ring | box | box − ring |
|---|---|---|---|
| 12 | 5.647 ± 0.011 | 6.774 ± 0.010 | +1.127 ± 0.014 |
| 16 | 7.413 ± 0.010 | 8.101 ± 0.010 | +0.688 ± 0.014 |
| 20 | 9.129 ± 0.012 | 9.464 ± 0.012 | +0.334 ± 0.017 |
| 24 | 10.811 ± 0.014 | 10.859 ± 0.015 | +0.048 ± 0.021 |
| 28 | 12.401 ± 0.019 | 12.232 ± 0.020 | −0.169 ± 0.027 |
| 32 | 13.988 ± 0.028 | 13.601 ± 0.030 | −0.388 ± 0.041 |

Local slopes per cell: ring 0.441, 0.429, 0.420, 0.398, 0.397 (± 0.004–0.008; 0.398 ± 0.013 to 36 from the file);
box 0.332, 0.341, 0.349, 0.343, 0.342. So the 2D analogue of "0.2087 against 0.231" is **0.40–0.44 (ring) against
0.34 (box)**, in the opposite order to gump: the rimmed edge is cheaper per cell, outlives the ring below
L ≈ 25 and dies sooner above. Caveat: my ring values and the file's scatter more than their errors (differences
+0.09, +0.05, +0.05, −0.13 at L = 20 … 32; χ² ≈ 19 on 6 for the ring, fine for the box); cause not found; pooled
errors are therefore optimistic by about a factor 1.8 on the ring.

**The two exits have their own exponential laws** [measured]. Split 1/τ by the bust share b (6 steps):
ln τ_flash = ln τ − ln b, ln τ_other = ln τ − ln(1 − b).

| | flash | other (fade) | logit b |
|---|---|---|---|
| ring | 0.296 ± 0.023 + (**0.4550 ± 0.0013**)·L, χ² 5.4/4 | 4.03 ± 0.05 + (**0.3274 ± 0.0023**)·L, χ² 7.4/4 | 3.74 − (0.1277 ± 0.0030)·L, χ² 8.7/4; b = ½ at L = 29.3 |
| box | 2.66 + 0.4005·L (χ² 12/4) | local slopes 0.284, 0.314, 0.322, 0.323, 0.336 (not straight: χ² 53/4) | 1.04 − (0.092 ± 0.003)·L |

- Robust to the window: with 4, 6, 12 steps the ring's flash slope is 0.459, 0.451, 0.448 and the other 0.335,
  0.329, 0.318; the box's 0.41–0.40 and 0.32–0.31 (unweighted fits, `table.py`).
- ring other − box other = +0.53, +0.71, +0.73, +0.75, +0.75, +0.85 (± 0.03–0.06): the fade costs the same per
  cell with or without ends and is about twice as fast with them (ln 2 = 0.69) [measured; why 2: not explained].
- box flash − ring flash = +1.74, +1.48, +1.22, +1.06, +0.97, +0.73: the ends tax the flash by a factor 5.7
  falling to 2 (part of the box's "flash" at small L is chance: living windows contain such a fall 0.11–0.004).
- Reading [conjectured, with a frozen forecast in PREDICTIONS block 2]: 1/τ_ring = e^(−0.30 − 0.455 L) +
  e^(−4.03 − 0.327 L). The ring's price is 0.455 where the flash carries the deaths and 0.33 beyond L ≈ 40
  (ln τ(40) = 16.90, (48) = 19.66, bust share 0.20 and 0.08). The file's L = 36 point (15.58 ± 0.045) is 0.11
  above this formula (15.47): a 2.5σ tension I could not resolve.

## 4. The exact one-row surrogate [proved = exact linear algebra; `sh run_exact.sh`, `python3 table.py`]

Row over two private coins (density 0.472) per cell; ring or open segment; quasi-stationary law and death rate
by power iteration (relative convergence 10⁻¹¹ in h).

EXACT_TABLE

- **Two prices do not converge by L = 20–24.** Ring local slope 0.523, 0.524, 0.527 at 16, 18, 20; segment 0.461,
  0.461, 0.459. The difference (0.062, 0.063, 0.068) is not decaying, so there is no e^(−L/ξ) to fit: in the
  range exact computation reaches, two end points change the price per cell by 13%. The gap
  ln τ_seg − ln τ_ring falls 1.45 → 0.67 from L = 8 to 20 and would vanish near L ≈ 30.
- **The same two exits, exactly.** Share of the death flux with a fall ≥ L/2 in its last K steps, K = 1, 2, 4, 6:
  ring 0.047, 0.289, 0.727, 0.884 at L = 20; segment 0.0000, 0.048, 0.330, 0.513 (living windows of 5
  transitions: 0.068 and 0.036). A death straight from a row at least half full (K = 1) carries 30% → 4.7% of a
  ring's deaths (L = 8 → 20) and less than 0.05% of a segment's from L = 9 on. Exact split at K = 6, slopes
  12–20: ring flash 0.550, ring other 0.420, segment flash 0.499, segment other 0.397; ring other − segment
  other = 0.58 … 0.76 (again about ln 2); logit of the ring's share falls 3.08 → 2.04 (−0.13 per cell), so the
  ring would leave the flash near L ≈ 36 and its price would then fall towards 0.40–0.42. This is the exact
  version of §3, and it says two prices at these sizes are neither a small-size transient of one route nor two
  asymptotic prices: they are the two exits' own per-cell prices, seen through a mixture that tips at a size set
  by the exits' constants.
- **The boom is shape-blind; the kill is not.** Upper tail of the quasi-stationary population,
  −ln P(n ≥ xL)/L, ring / segment at L = 20: 0.0629 / 0.0556 (x = 0.75), 0.184 / 0.173 (0.875), 0.3662 / 0.3522
  (full row). The difference in −ln P at x = 0.75 is 0.149, 0.167, 0.150, 0.146 at L = 8, 12, 16, 20: a constant,
  i.e. the same rate per cell with a prefactor e^0.15 in the segment's favour (its ends are denser: 0.709, 0.772,
  0.631 against 0.645). The segment is over-full MORE often than the ring and dies by flash far less: the ends
  survive the over-full generation. Same statement as gump's ("−ln P = 1.9 + ψ(x)·A, identical on tubes and wide
  faces"; "the rim line survives the over-full generation").

## 5. Other capped-threshold rows (exact; `sh run_other.sh`)

OTHER_TABLE

## 6. What this says about gump [conjectured]

1. "Capped threshold + a boundary with fewer neighbours ⇒ two exits, flash closed by the rim" holds in 2D and in
   its exact surrogate. Generic to the class as far as tested.
2. Which geometry is dearer per cell is NOT generic: it is the order of the two exits' prices. In 2D the flash
   costs 0.455 and the fade 0.33 (the cap needs 5 of an edge cell's 6 neighbours; in gump 6 of 9, so gump's
   over-fill is cheap), so rings look dear at small L and both shapes end on the fade's price. In gump the flash
   is the cheaper exit (0.2087 against about 0.213 for a wrapped face's no-bust route and 0.231 for the hull's
   fade), so wrapped faces keep it at every size and their bust share does not fall.
3. A test this suggests for gump: 1/τ = Σ over exits of e^(−a_i − c_i·A). The hull face's flash exit should
   cost 0.2087·A + (rim tax), with a tax that is sub-extensive (in 2D: a constant factor 2–6). If so the bust
   share of hull deaths must RISE with face size and the hull's price must eventually fall from 0.231 to
   0.2087; "no correction linear in the rim joins the two" would then be because the two numbers belong to
   different exits. Measure the hull's bust share at 45, 63, 84, 108 cells: a rising logit decides it.

## 7. Not checked

- Ring edges beyond L = 32 (36 from the file only); the forecast crossover to 0.33 above L ≈ 40 is untested.
- The 2–3σ scatter between my ring lifetimes and the file's (same protocol as far as I can tell).
- The ring is a strip of width 16; the cut channel ends 29 residences in 30 at L = 32, so ring states are young
  (mean residence 19,000 generations against τ = 1.1×10⁶). The box has no such channel.
- The split by "a fall ≥ L/2 within K steps" is a classifier, not a decomposition into disjoint routes; chance
  falls contaminate it at L ≤ 16 (living baseline up to 0.2). Slopes are stable under K = 4, 6, 12; constants move
  by 0.3–0.4.
- Exact segments have one code. Coin density fixed at 0.472. Exact runs stop at L = 22 (ring) / 24 (segment).
- Why the fade is twice as fast with ends; whether the box's fade slope (rising 0.28 → 0.34) converges to the
  ring's 0.327.

## Reproduce

```sh
cd research/blast/toy
python3 validate.py && python3 counts.py
sh run_bf.sh        # ring and box, L = 12..32: 8 min on one core
sh run_exact.sh     # exact rings and segments to L = 22 / 24: 10 min, 0.5 GB (waits for run_bf.sh's bf.done)
sh run_other.sh     # two more rules, exact: 3 min (waits for exact.done)
python3 anat.py > data/anat.txt; python3 table.py > data/tables.txt
```
