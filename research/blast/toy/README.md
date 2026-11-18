# blast/toy — do gump's two exits exist in its 2D relative? (agent `toy`, 2026-11-18)

Rule: cross2 B34/S234 ("alive next iff n + x ≥ 3, except n ≥ 5 dies"; `research/toy2d/`). The "face" is an edge
row of L cells. **Ring** = edge row of a strip 16 × L periodic along the edge (the analogue of a wrapped face);
**box** = edge of an L × L box (the analogue of a hull face: two ends at corners). Tags: [proved] (by enumeration
or exact linear algebra), [measured] (one code unless said; error = 1/√deaths or binomial), [conjectured].
Commands run from this directory; bulk output in `research/scratch/blast/toy/`; curated output in `data/`
(`data/tables.txt` = `python3 table.py`, `data/anat.txt` = `python3 anat.py`). Forecasts: `PREDICTIONS.md`
(block 1 frozen before any run: 3 hits, 4 misses; block 2 frozen before the last exact runs and unscored data).

## Verdict

**Yes: both exits exist in 2D and the rim closes the flash, as in gump. But in 2D the flash is the DEARER exit
per cell, so "two prices" there is a crossover between exits, not two asymptotic prices.**

1. A ring edge dies by boom and bust: the row over-fills (peak 19.4 of 24 against a living mean of 13.9), the cap
   kills it to 1–2 cells, they starve; flat along the ring. A box edge fades over 6–8 generations from the middle
   towards its corners, with FEWER over-full generations before death than a living window has (0.8 times),
   where the ring has 3.6–4 times as many.
2. The ring's deaths are a mixture of two exits with their own exponential laws: flash
   ln τ = 0.30 + **0.455**·L and no-flash 4.03 + **0.327**·L. The flash share falls like a logistic in L (0.90 at
   12 cells, 0.47 at 32; logit slope −0.128 ± 0.003 per cell, the same with a second classifier; one half at
   L ≈ 29), and the ring's local price falls with it, 0.441 → 0.397, towards the box's steady 0.34. The measured
   "0.416 (ring) against 0.343 (box)" of `research/toy2d` is that mixture. The box edge outlives the ring edge
   below L ≈ 25 and dies sooner above (ln τ_box − ln τ_ring = +1.13 … −0.39 at L = 12 … 32).
3. The exactly solved one-row surrogate has the two prices with no chaos beneath and to four digits: open
   segments 0.4591, 0.4594, 0.4593 per cell at L = 21, 22, 24 (converged), rings 0.520–0.528 at L = 16–22 (not
   converging to it: the difference 0.060–0.069 does not decay, so there is no e^(−L/ξ) to fit). Its ring is
   still 88% flash at L = 20. So in one dimension, where a rim is two points, two prices persist for as long as
   the wrapped shape's deaths go through the flash, and they end by a change of exit (2D brute force: at L ≈ 30,
   over a width of 1/0.128 ≈ 8 cells), not by a correlation length.
4. The boom is shape-blind and the kill is not, exactly as in gump: the surrogate's segment is over-full MORE
   often than its ring (same rate per cell, prefactor e^0.15) and dies straight from a half-full row less than
   0.05% of the time against 5–30% for the ring.

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
- `python3 mc_check.py L ring` (plain numpy Monte Carlo of the surrogate, an independent code): segment L = 12:
  ln τ 7.7379 ± 0.011 and 7.7505 ± 0.008 (exact 7.7402), flash share (6 steps) 0.698 ± 0.005 and 0.707 ± 0.004
  (exact 0.7046); ring L = 12: 6.4220 ± 0.009 (6.4169), 0.9548 ± 0.0018 (0.9560); segment L = 16: 9.567 ± 0.017 and
  9.552 ± 0.012 (9.5731), 0.578 ± 0.008 and 0.600 ± 0.006 (0.6022; the first is 2.9σ low, the second seed is not).

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
- **Second classifier** (`python3 boom.py` → `data/boom.json`): "boom" = the row at least 0.8·L full in one of
  its last 6 living generations. Ring deaths: 0.886, 0.828, 0.731, 0.555, 0.448, 0.353 at L = 12 … 32 (living
  windows 0.53, 0.46, 0.38, 0.14, 0.12, 0.097): enriched 3.6–4 times at L ≥ 24, logit slope −0.13 per cell. Box
  deaths: 0.529, 0.379, 0.286, 0.151, 0.107, 0.097 (living 0.62, 0.53, 0.45, 0.18, 0.16, 0.12): BELOW chance at
  every size. So the box's "bust6" above is mostly chance falls inside a fade; the box has in effect one exit.
- The contrast in bust share is 2–3, not gump's 40 (0.6 against 0.016), and the ring's share FALLS with L (gump's
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
- ring other − box other = +0.53, +0.71, +0.73, +0.75, +0.75, +0.85 (± 0.03–0.06): the ring's no-flash exit is
  about half as fast as the box edge's fade at every size (ln 2 = 0.69) [measured; why 2: not explained], and
  its price (0.327 ± 0.002; 0.318–0.335 over classifiers) is at or slightly below the box's (0.343 ± 0.003).
- The box's total price does not move (0.332–0.349) while its bust6 share falls from 0.49 to 0.15: so the box's
  "flash" line is not a second exit but chance falls (see the boom classifier, §2); likewise the exact segment
  (§4), whose price is constant to four digits while its share falls. The split is a real decomposition only
  for the ring, where the two classes differ in kind (bimodal population two generations before the end).
- Reading [conjectured, with a frozen forecast in PREDICTIONS block 2]: 1/τ_ring = e^(−0.30 − 0.455 L) +
  e^(−4.03 − 0.327 L). The ring's price is 0.455 where the flash carries the deaths and 0.33 beyond L ≈ 40
  (ln τ(40) = 16.90, (48) = 19.66, bust share 0.20 and 0.08). The file's L = 36 point (15.58 ± 0.045) is 0.11
  above this formula (15.47): a 2.5σ tension I could not resolve.

## 4. The exact one-row surrogate [proved = exact linear algebra; `sh run_exact.sh`, `python3 table.py`]

Row over two private coins (density 0.472) per cell; ring or open segment; quasi-stationary law and death rate
by power iteration (relative convergence 10⁻¹¹ in h).

<!--EX-->
| L | ln τ ring | ln τ segment | segment − ring | slope ring | slope segment | flash share (6 steps) ring | segment |
|---|---|---|---|---|---|---|---|
| 8 | 4.4000 | 5.8468 | +1.4468 |  |  | 0.976 | 0.767 |
| 9 | 4.9554 | 6.2863 | +1.3310 | 0.5554 | 0.4395 | 0.968 | 0.697 |
| 10 | 5.3838 | 6.7641 | +1.3803 | 0.4284 | 0.4777 | 0.967 | 0.754 |
| 11 | 5.8667 | 7.2587 | +1.3920 | 0.4829 | 0.4947 | 0.960 | 0.679 |
| 12 | 6.4169 | 7.7402 | +1.3233 | 0.5502 | 0.4814 | 0.956 | 0.705 |
| 13 | 7.0061 | 8.2010 | +1.1949 | 0.5892 | 0.4608 | 0.945 | 0.637 |
| 14 | 7.5765 | 8.6551 | +1.0787 | 0.5704 | 0.4542 | 0.939 | 0.654 |
| 15 | 8.1122 | 9.1123 | +1.0002 | 0.5357 | 0.4572 | 0.927 | 0.591 |
| 16 | 8.6350 | 9.5731 | +0.9381 | 0.5228 | 0.4608 | 0.923 | 0.602 |
| 17 | 9.1571 | 10.0344 | +0.8773 | 0.5221 | 0.4613 | 0.909 | 0.544 |
| 18 | 9.6834 | 10.4946 | +0.8112 | 0.5263 | 0.4602 | 0.905 | 0.554 |
| 19 | 10.2118 | 10.9538 | +0.7419 | 0.5284 | 0.4591 | 0.888 | 0.502 |
| 20 | 10.7379 | 11.4127 | +0.6747 | 0.5261 | 0.4589 | 0.884 | 0.513 |
| 21 | 11.2602 | 11.8718 | +0.6115 | 0.5223 | 0.4591 | — | — |
| 22 | 11.7800 | 12.3311 | +0.5511 | 0.5198 | 0.4594 | — | 0.476 |
| 24 | — | 13.2497 | — | — | 0.4593 | — | — |
<!--/EX-->

- **Two prices, exact, and not converging.** Segment local slope per cell 0.4608, 0.4613, 0.4602, 0.4591, 0.4589,
  0.4591, 0.4594 at L = 16 … 22 and 0.4593 over 22–24: the open row's price is **0.4593 ± 0.0003**. Ring: 0.5228,
  0.5221, 0.5263, 0.5284, 0.5261, 0.5223, 0.5198 at L = 16 … 22 (it wobbles with L; at L ≤ 15 between 0.43 and
  0.59). The difference, 0.060–0.069, does not decay over L = 16–22: no e^(−L/ξ) can be fitted, i.e. ξ is not
  "a few cells" (the last three ring slopes fall by 0.003 per cell: the start of the bend or the next wobble, I
  cannot tell). The gap ln τ_seg − ln τ_ring falls 1.447 → 0.551 from L = 8 to 22 and would vanish near L ≈ 31.
- **Flash share of the death flux, exact** (a fall ≥ L/2 in the last K steps; K = 1, 2, 4, 6): ring 0.047, 0.289,
  0.727, 0.884 at L = 20; segment 0.0000, 0.048, 0.330, 0.513 (living windows of 5 transitions: 0.068 and 0.036).
  A death straight from a row at least half full (K = 1) carries 30% → 4.7% of a ring's deaths (L = 8 → 20) and
  less than 0.05% of a segment's from L = 9 on: an end cell with its two neighbours alive cannot die. The ring's
  logit (K = 6) falls 3.08 → 2.04 from L = 12 to 20 (−0.13 per cell, the brute force's slope), which puts its
  change of exit near L ≈ 36, beyond exact reach. I do NOT trust the split of the surrogate's rates into two
  exponentials (`data/tables.txt` prints it): at a share of 0.9 the "other" class is mostly misclassified flash,
  and the segment's share falls 0.60 → 0.48 while its price stays 0.4593, so there the classifier counts chance.
- **The boom is shape-blind; the kill is not.** Upper tail of the quasi-stationary population,
  −ln P(n ≥ xL)/L, ring / segment at L = 20: 0.0629 / 0.0556 (x = 0.75), 0.184 / 0.173 (0.875), 0.3662 / 0.3522
  (full row). The difference in −ln P at x = 0.75 is 0.149, 0.167, 0.150, 0.146 at L = 8, 12, 16, 20: a constant,
  i.e. the same rate per cell with a prefactor e^0.15 in the segment's favour (its ends are denser: 0.709, 0.772,
  0.631 against 0.645). The segment is over-full MORE often than the ring and dies by flash far less: the ends
  survive the over-full generation. Same statement as gump's ("−ln P = 1.9 + ψ(x)·A, identical on tubes and wide
  faces"; "the rim line survives the over-full generation").

## 5. Other capped-threshold rows (exact; `sh run_other.sh`)

<!--OT-->
**Rule A** (range 3, 3 coins of density 0.5, alive iff n + x ≥ 4 and n ≤ 6; a segment's end cell has n ≤ 6: never overcrowded):

| L | ln τ ring | ln τ segment | segment − ring | slope ring | slope segment | flash share (6 steps) ring | segment |
|---|---|---|---|---|---|---|---|

**Rule B** (range 1, 2 coins of density 0.5, alive iff n + x ≥ 2 and n ≤ 2; a segment's end cell has n ≤ 3: it CAN be overcrowded):

| L | ln τ ring | ln τ segment | segment − ring | slope ring | slope segment | flash share (6 steps) ring | segment |
|---|---|---|---|---|---|---|---|
<!--/OT-->

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
