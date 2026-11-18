# THEORY: does a two-variable map (face P, layer beneath B) give the price per cell with nothing fitted?

Investigator `ref-anatomy`, 2026-11-18, 04:20–04:55 UTC. Labels: **[measured]** (gump, my stepper), **[computed]**
(from the measured map, nothing fitted), **[conjectured]**. Nothing is proved. `REVIEW.md` is untouched.

## The answer

**No for the price, yes for the route and for the order of the shapes.** A chain on (P, B) with the measured
one-step mean and covariance and Gaussian noise, nothing fitted:

- finds the right route on a wrapped face by itself: a face at its normal filling over an *under-full* layer
  beneath, one jump up of both layers, the fall, then starvation: (33,25) → (46,42) → (16,7) → … (measured means:
  (33.3, 25.2) → (48.8, 39.9) → (11.2, 9.9)); and on the hull face a fade of 13 generations with no over-full
  generation at all (measured: about 10, 5–16) **[computed]**;
- gives a minimum action of **0.160 per cell** on the wide torus (0.1595–0.1625 at 48 to 108 cells; exactly linear
  in A, intercept 0.03), against gump's 0.2087: **23% short**. The exact lifetime of the same chain rises by 0.176
  per cell (48 to 108 cells, 63-cell map carried at equal fillings) or 0.184 (48, 63, 84 with each size's own
  living map): 12–16% short **[computed]**;
- gives **0.231 per cell** on the 63-cell hull face (gump's hull price from second differences: 0.231; its
  ln τ/A at 63 cells: 0.216), i.e. hull > torus as measured, but by a factor 1.45 where gump has 1.11;
- gives the tube a lower action than the wide torus at equal size (right sign, wrong size; see iv).

**Why it falls short [measured]:** the boom is not a two-layer event. Before a fatal fall the first five layers hold
48.8, 39.9, 34.5, 30.7, 28.7 cells (stationary 32.5, 27.3, 25.5, 26.1, 26.0), and one generation earlier the face
is normal and layers 2–5 are all *under*-full (25.2, 22.3, 24.0, 24.8). Two variables do not close in the
over-full state (the fall of P depends on C with slope −0.24 cell per cell at fixed (P, B)), and the Gaussian is
thinner than the true one-step upper tail by a further 0.012–0.017 per cell.

## 0. What is measured, what is computed, what is fitted

- **Measured** (`fd2.c`, same stepper as `fd.c`; `validate_fd2.out`: identical to the oracle for 1,100 generations
  on t63, h63, t84, t48, tube60, tube84; a swapped neighbour fails at generation 12 and 6). `sh run2.sh` (7
  minutes, seeds 2026111811–16): for every face-generation after burn-in with (P, B, C) the populations of the
  face layer, the layer beneath and the third layer, cell (P, B) accumulates n and the first and second moments
  of (P′, B′), and C with its products (closure test); also the full histogram of (P′, B′) from a "launch box"
  |P − P*| ≤ 1, |B − B*| ≤ 2 round the route's launch state.

  | vessel | cells | exposure | deaths | ln τ here | anchor | cells (P,B) with n ≥ 200 |
  |---|---:|---:|---:|---|---|---:|
  | t63 torus (1,4),(0,21) | 63 | 1,269,293,463 | 4,987 | 13.140 ± 0.014 | 13.1622 | 1,902 |
  | t48 torus (4,0),(0,4) | 48 | 318,932,313 | 29,489 | 9.982 ± 0.006 (see §5: settled replicas) | 9.9251 | 1,324 |
  | t84 torus (1,4),(0,28) | 84 | 813,134,832 | 42 | 17.47 ± 0.15 | 17.5387 | 2,121 |
  | h63 hull radius 11 | 63 | 385,922,425 | 3,614 | 13.658 ± 0.017 | 13.633 | 1,830 |
  | tube60 (1,8),(0,20) | 60 | 635,761,742 | 5,162 | 12.414 ± 0.014 | 12.423 | 1,741 |
  | tube84 (1,12),(0,28) | 84 | 528,451,448 | 37 | 17.17 ± 0.16 | 17.3175 | 2,087 |

- **Computed** (`python3 theory.py` → `out/theory.txt`; `theory2.py` → `out/theory2.txt`; `theory3.py` →
  `out/theory3.txt`). The model is a Markov chain on the integer grid (P, B) ∈ [0, A]²; from (P, B) the step is a
  bivariate Gaussian with the measured mean and covariance of that cell, rounded to the grid; P′ < 0.5 is death;
  states are the cells with n ≥ 200 (mass sent elsewhere is renormalised away; in the living state it is
  10⁻⁴–10⁻⁸ per step). Two outputs: the **minimum action** S = min over paths from the living mode to death of
  Σ ½ dᵀΣ⁻¹d (value iteration; the route is its argmin), and the chain's **exact lifetime** (quasi-stationary
  death rate by power iteration). For a size other than the map's, mean/A and covariance/A are carried over at
  equal fillings x = P/A, b = B/A (bilinear).
- **Fitted: nothing.** Choices that are mine: n ≥ 200, the rounding and the 0.5 threshold for death, bilinear
  carrying, the launch boxes.
- **A warning about the lifetime at the map's own size.** Any one-step kernel estimated from a stationary run
  reproduces that run's death rate identically if used whole; the Gaussian chain at its own size differs from that
  only by the Gaussian shape. So 13.07 against 13.16 at 63 cells is *not* a test. The tests are the slope with A,
  the route, and the contrasts between shapes.

## 1. The map **[measured]**

At the living centre, per cell (variance of P′, of B′, covariance, each divided by A): 0.318, 0.297, 0.095 (48
cells); 0.330, 0.299, 0.100 (63); 0.342, 0.306, 0.105 (84); hull 63: 0.292, 0.329, 0.120; tube60: 0.335, 0.302,
0.102; tube84: 0.355, 0.319, 0.113.

**Collapse across sizes (wide tori): close, not exact, and the corrections have a pattern.** The smaller face's map
carried to the larger grid, minus the larger face's own, over cells with n ≥ 2,000 in both:

| | drift of x, living core (weighted) | over-full cells (x ≥ 0.70) | drift of b, living / over-full | variance of P′, carried / own, living / over-full |
|---|---|---|---|---|
| 48 → 63 | +0.0075 (rms 0.0077) | +0.0016 (rms 0.0024) | +0.0056 / +0.0025 | 0.963 / 0.973 |
| 63 → 84 | +0.0059 (rms 0.0060) | +0.0021 (rms 0.0024) | +0.0047 / +0.0026 | 0.963 / 0.969 |
| 48 → 84 | +0.0139 (rms 0.0141) | +0.0044 (rms 0.0051) | +0.0105 / +0.0054 | 0.928 / 0.934 |

So the drift is a function of (x, b) plus about **1.5 cells / A** in the living core (0.0075, 0.0059, 0.0139 divided
by the differences of 1/A give 1.51, 1.49, 1.56 cells) and about 0.4 cell / A when over-full; and the covariance is
**not** ∝ A: per cell it grows by 3.7% from 48 to 63 and again from 63 to 84 (∝ A^1.13 over this range, or a
1/A correction of 6–8 cells; three sizes cannot tell). [conjectured] Both are what conditioning on two global
numbers does to a system of A cells; neither changes the asymptotic slope of S if they are 1/A corrections, but a
variance that kept growing would *lower* the price.

**Tube against wide torus at equal size: the same map.** tube84 against t84: drift of x −0.0010 (rms 0.0016) in the
living core, 0.0000 (rms 0.0006) over-full; variance of P′ 1.031 times the torus's in the living core, 1.001
over-full. tube60 against t63: drift within 0.0006, variance 1.013. The tube's only visible difference is 3% more
one-step noise round the living state.

**Hull against torus: a different map.** Carried to the torus grid the hull's drift of x differs by +0.15 in the
over-full cells (no cliff: `REVIEW.md` §3a) and its variance there is 2.4 times the torus's.

**Closure: two variables are enough in the living state, not in the over-full one.** Slope of P′ on the third
layer's population C at fixed (P, B), weighted by n: −0.041 (t63), −0.044 (t48), −0.039 (t84), −0.014 (hull); of
B′ on C: −0.098, −0.090, −0.092, −0.068. In over-full cells (x ≥ 0.70): P′ on C −0.24 (t63), −0.25, −0.23, hull
−0.20; B′ on C −0.31, −0.32, −0.30, −0.26.

**How deep the boom is** (`out/theory3.txt`; full states of the review's windows, 63-cell torus; layers 1–5,
stationary 32.5, 27.3, 25.5, 26.1, 26.0):

| | generation before the peak | the over-full generation | the generation after |
|---|---|---|---|
| fatal fall of half the face (2,262) | 33.3, 25.2, 22.3, 24.0, 24.8 | 48.8, 39.9, 34.5, 30.7, 28.7 | 11.2, 9.9, 13.1, 20.4, 23.6 |
| non-fatal fall of half (4,000) | 33.0, 26.0, 23.3, 24.8, 25.4 | 48.9, 34.5, 29.5, 27.5, 26.7 | 14.9, 18.6, 20.6, 24.9, 25.9 |
| over-full generation, P ≥ 46 (4,000) | 33.0, 27.0, 24.7, 25.6, 25.8 | 46.8, 30.8, 27.0, 26.5, 26.4 | 23.0, 23.6, 23.5, 25.9, 26.1 |

The same on the tube (46.4, 37.9, 33.0, 29.3, 27.3 at the peak of a fatal fall). The fatal event is a surge of at
least five layers launched from a state in which the face is normal and every layer beneath it is thin; what
separates fatal from non-fatal is depth (layers 2–5), not the face (48.8 against 48.9).

## 2. The Gaussian chain and its minimum action **[computed]**

| map, at size | minimum action S | S / A | exact ln τ of the chain | gump ln τ |
|---|---|---|---|---|
| t63, 63 (own) | 10.052 | 0.1595 | 13.070 | 13.1622 |
| t63 carried to 48 | 7.776 | 0.1620 | 10.883 | 9.9251 |
| t63 carried to 60 | 9.672 | 0.1612 | 12.927 | 12.536 (wide-face line) |
| t63 carried to 84 | 13.653 | 0.1625 | 17.151 | 17.5387 |
| t63 carried to 108 | 17.348 | 0.1606 | 21.257 | 22.5405 |
| t48 own (P ≥ 17) + t63 below, 48 | 7.641 | 0.1592 | 10.570 | 9.9251 |
| t84 own + t63 below, 84 | 13.788 | 0.1641 | 17.212 | 17.5387 |
| tube60, 60 (own) | 9.422 | 0.1570 | 12.293 | 12.423 |
| tube84 own + t63 below, 84 | 13.404 | 0.1596 | 17.127 | 17.3175 |
| tube84 own + tube60 below, 84 | 13.327 | 0.1587 | 16.612 | 17.3175 |
| h63, 63 (own) | 14.572 | 0.2313 | 14.776 | 13.633 |
| h63 carried to 45 / 84 (not justified: the rim's share changes) | 10.505 / 19.441 | 0.2334 / 0.2314 | 10.946 / 19.643 | 9.819 / 18.141 |

Slopes over 48–108 cells with the 63-cell map: S 0.1608 per cell (intercept +0.03); chain ln τ 0.1756 (intercept
+2.29, not smooth: 0.146, 0.194, 0.171 between successive sizes). With own living maps at 48, 63, 84: 0.167 and
0.197, 0.184 overall. Gump: 0.2087 (63–126), intercept 0.01. (The own-map rows for t84 and tube84 alone are not
given: with 42 and 37 deaths their low cells are empty and the route is cut off.)

**Routes** (P, B) and the cost of each step:

- t63: (33,28) → (35,30) → (33,25) → **(46,42)** → (16,7) → (11,6) → (6,6) → (4,6) → (3,7) → (2,9) → (1,11) → empty;
  costs 0.07, 0.14, **5.79**, 1.58, 1.20, 0.64, 0.36, 0.05, 0.07, 0.15, 0.00. The chain primes itself: it first lets
  the layer beneath thin to 25 (cost 0.2), then jumps. At 84 and 108 cells the same shape:
  (44,34) → (61,56) → (22,9) → …; (57,43) → (78,72) → (29,12) → ….
- h63: (32,28) → (30,27) → (27,25) → (23,21) → (19,17) → (15,15) → (12,14) → (9,14) → (6,15) → (4,17) → (3,20) →
  (2,24) → (1,27) → empty; costs 0.17, 0.62, 1.79, 2.78, 2.38, 1.59, 1.31, 1.40, 1.06, 0.47, 0.47, 0.41, 0.13: no
  step dominates, the layer beneath recovers while the face goes on down.

## 3. The four comparisons asked for

**(i) Action per cell against 0.2087, and against the measured split.** 0.160 (minimum action), 0.176–0.184 (chain).
Split of S at 63 cells: up to and including the fall 7.58 = **0.120 per cell** (measured rarity of the fall: 0.130);
after it 2.47 = **0.039 per cell** (measured fatality: 0.088). The Gaussian action of the *measured* mean route
(33,25) → (49,40) → (11,10) → (6,10) → (3,12) → (2,15) → (1,19) is 6.38 + 1.49 + 1.75 + 1.11 + 0.25 + 0.39 + 0.20 =
11.55 = 0.183 per cell: the true route is 1.5 nats dearer than the Gaussian optimum, and still short of 0.2087.
Replacing the Gaussian end-game by the measured chance of death q(P) below 8, 12, 16 or 20 cells (`REVIEW.md`'s
table; B-blind) gives S = 10.45, 10.65, 10.95, 11.55 at 63 cells and slopes 0.1635, 0.1625, 0.1616, 0.1624: the
chain then spends about 5 on the kill (0.08 per cell, near the measured 0.088) but buys a cheaper, shallower
boom, and the total hardly moves. **The Gaussian is too generous on the jump**, as the PI said, but by less than 1.27: landing
exactly on the route's (46,42) from the launch box happens with −ln probability 11.57 (2,318 times in 2.4·10⁸)
against a Gaussian −ln density of 10.81, +0.76 nats (ratio of exponents 1.13 once the normalisation 4.78 is taken
off); at 84 cells (65,53): 15.11 against 13.65, +1.46 nats (1.17). That is +0.012 to +0.017 per cell: with it the
minimum action is about 0.175. Marginal upper tail of P′ alone from the launch box: 1.05–1.11 times the Gaussian
exponent at P′ = 45–50 of 63.

**(ii) The route.** Right in kind and in its first two states, coarse after: launch (33,25) against the measured
(33.3, 25.2); peak (46,42) against (48.8, 39.9); landing (16,7) against (11.2, 9.9); then 7 more generations
against a measured median of 4 (2–8). The model's peak is lower in the face and higher beneath, its landing higher
in the face: it under-uses the face and, having no third layer, over-uses B.

**(iii) The hull face.** Its map has no cliff, and the chain's minimum action is 14.57 = 0.2313 per cell, 1.45
times the torus's; the route is a 13-generation fade through (23,21), (15,15), (9,14) with no over-full
generation. The chain's exact lifetime is 14.78 against 13.633: at its own size, where the comparison is nearly
forced, the Gaussian is too *stingy* by 1.1 (on the hull the one-step lower tail is fatter than Gaussian: landing on
(19,17) from the living box has −ln 9.95 against 10.66). Carried to 45 and 84 cells the chain's slopes are 0.213
and 0.232 per cell against gump's 0.212 and 0.215. So: higher per cell, yes; a ten-generation fade, yes; "near
0.231", yes (0.2313), though with the torus 23% short I do not read that agreement as more than half luck.

**(iv) The tube.** Its map is the wide torus's to 0.001 in drift; it has 3% more one-step variance in the living
core and none over-full. That alone lowers the action: at 84 cells, same low-population map for both, S = 13.40
(tube) against 13.79 (torus), chain ln τ 17.13 against 17.21 (−0.085; gump −0.221); with the tube's own
low-population map −0.60. At 60 cells S = 9.42 against 9.67. Right sign, the size not pinned (between 0.4 and 3
times the measured discount, depending on which low map is used).

## 4. Where the missing 0.03–0.05 per cell is **[conjectured, with the measurements that point there]**

1. **Depth.** The fatal surge fills five layers (§1) and is launched from four thin ones. The two-variable chain
   pays for P and B only, and treats C's effect on the fall as free noise (the fall (46,42) → (16,7) costs it
   1.58). A chain on (P, B, C) is the next thing to compute; (P, B, C, D) may be needed.
2. **The jump's tail**: +0.012 to +0.017 per cell, measured (i).
3. **The collapse corrections**: a covariance per cell that grows 3.7% per 30% of area lowers the Gaussian price
   with size unless it saturates; the drift's 1.5 cells / A raises the intercept only.
4. Not the end-game: measured q(P) in place of the Gaussian kill changes the slope by 0.001–0.003.

A reading of the whole [conjectured]: the face's lifetime is the cost of a rare *vertical* event (a column of
thin layers filling at once) on wrapped faces, where the cliff turns over-filling into emptying, and of a slow
*horizontal* one (a fade the layer beneath cannot stop) on the hull face, whose rim removes the cliff. A local
large-deviation theory of the first needs the depth profile as its variable, not the face.

## 5. Not checked, and known defects

- **Settled replicas spoil the 48-cell map's low cells.** `fd2.c` does not restart replicas whose slab has gone
  static with a few face cells alive (0.12% of lives at 48 cells; `fd.c` does, every 2,520 generations). They pile
  up (ln τ 9.982 instead of 9.925) in a few cells such as (7,7). I therefore use the 48-cell map only for P ≥ 17
  and in the collapse table; its "low" row there is contaminated. No such lives were seen at 60 cells and above
  in the review's runs, but fd2 would not have noticed one.
- The Gaussian chain's lifetime at the map's own size is nearly forced (§0). The slopes rest on carrying a map
  across sizes, which §1 shows is good to 0.006 in drift and 4% in variance per step, not better.
- A grid of integers at 48–108 cells is far from a large-deviation limit: the chain's ln τ exceeds S by 3.0–3.9
  (prefactors), and its slope is not smooth. No continuum limit was taken.
- No three-variable chain. No measured-kernel chain (it would reproduce τ by construction and test nothing).
- The hull map carried to other sizes ignores that the rim's share of the face changes.
- n ≥ 200, the 0.5 threshold and the bilinear carrying were not varied. `theory.py` has had no second reader.
- Agent `boom`'s directory was not read; agreement or disagreement with it is unknown to me.

## 6. Forecasts (`PREDICTIONS.md` block 2, commit 88f530f, before any joint tally)

| # | forecast | result | |
|---|---|---|---|
| 1 | Gaussian minimum action 0.16 per cell (0.12–0.20), below 0.2087 | 0.1595 | hit |
| 2 | chain ln τ at 63 cells 11.0 (9.5–12.5) | 13.07 | miss: I had not seen that it is nearly forced |
| 3 | torus route: one generation at x ≥ 0.70, then one at x ≤ 0.25 | 0.730, then 0.254 | hit in kind |
| 4 | hull action per cell higher; ratio 1.05–1.25; no over-full generation, ≥ 6 generations | higher; 1.45; none, 13 | two of three |
| 5 | drift collapses to 0.01, covariance × A to 10% | 0.006–0.008 between neighbours, 0.014 for 48 against 84; 4–7% | half; the 1/A pattern was not foreseen |
| 6 | C matters < 0.1 in ordinary generations, ≥ 0.15 over-full | −0.04; −0.24 | hit |
| 7 | tube map = torus map to 0.005; so no tube discount from the action | 0.001; a discount of the right sign from 3% more noise | first half hit, second miss |
