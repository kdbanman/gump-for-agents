# blast/model: models of the face-death rate against every number on file (2026-11-18)

Agent `model` of the blast. Brief: `../BRIEF-COMMON.md`. Forecasts: `PREDICTIONS.md` (blocks M1–M5, each committed
before the data it concerns was opened). Labels: **[measured]**, **[fitted]**, **[conjectured]**, **[post hoc]**.
Nothing here is proved. The session was cut to about 70 minutes; "Not checked" at the end is long.

## The upper tail (added 03:57 on the PI's second brief, after agent `anatomy`'s boom and bust)

**Does the over-full tail explain the wrapped price? About 40–50% of it (the boom), and none of the shape
dependence. The rest is the kill after the fall, which is the old tail price again; and both the boom and the kill
from a given low population are blind to tube against wide, so the tube's discount is made in between.**

a. **[measured] The over-full tail obeys a clean law per cell, and it is the same law on tubes and on wide faces.**
   From the stationary histograms (1.5 × 10⁸ samples each; wide faces of 57–111 cells, loop² 12 tubes of 54–120
   cells), at fixed filling x = P/A:

   | x = P/A | −ln π(xA), wide faces | −ln π(xA), tubes of loop² 12 | Gaussian with the stationary ρ, s² |
   |---|---|---|---|
   | 0.70 | 1.93 + 0.0561·A (rms 0.01) | 1.93 + 0.0560·A | 0.044·A |
   | 0.73 | 1.90 + 0.0755·A (0.02) | 1.92 + 0.0750·A | 0.060·A |
   | 0.76 | 1.87 + 0.0984·A (0.02) | 1.83 + 0.0987·A | 0.078·A |
   | 0.79 | 1.75 + 0.1265·A (0.02) | 1.69 + 0.1273·A | 0.099·A |

   So the boom has a price per cell ψ(x) that is 1.27 times the Gaussian one (the distribution is skewed: its
   upper side is thin, its lower side fat), with a constant of about +1.9 nats. At equal area the tube and the wide
   face have the same over-full probabilities: ln P(P ≥ 0.73A) = −6.866 / −6.874 (66 cells), −8.103 / −8.123 (84),
   −9.500 / −9.521 (108); the three 96-cell faces with one loop² of 12, 13, 16: −9.175, −9.190, −9.168, while
   their lifetimes differ by 0.07–0.19. **The upper tail does not carry the shape dependence, nor the bending
   with tube length.** The tube's larger variance per cell (0.402 against 0.378–0.388) does not grow with length
   and sits entirely on the low side: at 0.40–0.55 P̄ a tube is e^0.26, e^0.48, e^0.86 times as likely as the wide
   face of the same 66, 84, 108 cells (`pairs.py`), 2.1–2.25 times its lifetime discount in ln τ; the tube's tail
   below that is steeper and gives half of the lead back. `python3 research/blast/model/upper.py`, `pairs.py`.

b. **[measured] 1/τ = Σ_P π(P)·g_L(P) (exact for any lag L; g_L(P) = chance that a face with population P is dead
   exactly L generations later), 48-cell torus, 48,059 deaths** (`ex5.c`, `boom.py`): four generations before death
   18.6% of dying faces are over-full (P ≥ mean + 2 sd = 34 of 48) against 1.67% of living ones; summed over lags
   2–9 the excess is 0.59 (anatomy's count of deaths with a half-face fall: 0.572). The integrand peaks at
   P* = 36 (0.75 A, +2.5 sd), where −ln π = 6.12 and −ln g₄ = 7.11. **The fall map** (mean population one
   generation after filling x): x = 0.70, 0.75, 0.80, 0.85, 0.90 → 0.42, 0.36, 0.29, 0.19, 0.12 of A, and the chance
   of landing below half the mean is 0.012, 0.08, 0.34, 0.89, 0.995. g₄ rises by e^0.85 falling to e^0.4 per extra cell of
   boom (1.5 × 10⁻⁴, 8.2 × 10⁻⁴, 3.2 × 10⁻³, 9.6 × 10⁻³, 3.1 × 10⁻² at P = 34, 36, 38, 40, 43) while π falls by
   e^(−0.7) steepening to e^(−1.4) per cell: the optimum is where the two slopes meet (a tangent construction on the upper side).
   **63-cell torus (5,028 deaths): the same picture at the same fractions.** 19.7% of dying faces are over-full
   four generations before death (9.7% above mean + 3 sd, against 0.048% of living faces); the excess summed over
   lags 2–9 is 0.68; the integrand peaks at P* = 47 (0.75 A), −ln π = 7.37, −ln g₄ = 9.34; the fall map is
   0.75, 0.79, 0.83 → 0.36, 0.29, 0.23 of A, as at 48 cells: **the fall is a function of the filling alone.**
   From 48 to 63 cells the peak's two factors grow by 0.083 per cell (boom) and 0.149 per cell (kill): 0.232
   together against 0.215 for ln τ between the same two faces.
   Only 11–14% of the visits to 10–14 cells come straight from an over-full generation, against 57% of the deaths:
   at equal count the scattered survivors of a bust are roughly 8 times as deadly as a face that thinned
   [inferred from marginals, not measured per death].

c. **[measured] A hull face has no such route, and its fall map shows why.** 45 cells (35,637 deaths) and 63 cells
   (2,442 deaths): the over-full share of dying faces at every lag 1–12 is at most the stationary share (at most
   0.017 against 0.018; at most 0.025 against 0.019). The fall map of the hull stops: x = 0.80, 0.85, 0.90 → 0.48, 0.44,
   0.39 of A at 45 cells (0.46, 0.40 at 63 cells) where the torus's reaches 0.29, 0.19, 0.12; the chance of landing
   below half the mean from x = 0.85 is 0.005–0.011 on a hull against 0.89 on the torus. The hull's dying faces
   fade instead: mean population 27, 23, 16, 10, 4 at 12, 9, 6, 4, 2 generations before death (63 cells).

d. **[fitted from three sizes, anatomy's table and item a] The price of the bust route splits about 0.08–0.10 for
   the boom and 0.11–0.13 for the kill.** The living rate of half-face falls (anatomy §2: 0.0075, 0.0015, 0.0009
   at 48, 63, 75 cells, read here as per 10 generations) falls by 0.079 per cell overall (0.107 and 0.043 in the two
   steps), which is ψ(0.735) of item a (0.079); the chance that such a fall ends in death is then 0.037, 0.0075,
   0.0011 (−0.106 and −0.16 per cell; anatomy's errors not propagated). The kill is
   the tail again: q(n) of the dip table at the survivors' count gives 0.049 at 9 cells (48-cell face) and 0.010
   at 12 cells (63-cell face), −0.103 per cell. So c_bust ≈ ψ(x*) + κ with ψ measured from the living state alone
   (no fitted number) and κ still measured from deaths: **the upper tail gives 40–50% of 0.2086; the other half is
   the same quantity nobody can derive yet, the price λ ≈ 0.42–0.44 per surviving cell, now applied to about 0.2–0.3 A
   scattered survivors instead of 0.5 A.** As a formula, min over x of [ψ(x) + λ·s(x)] with s the fall map does
   not work at 48 cells: it gives 0.275 at x = 0.71–0.75 against ln τ/A = 0.207; the difference (3.3 nats) is the
   number of (P, lag) cells that contribute and the spread of the fall, not a price.

e. **[fitted] Two routes do not give the hull's 0.231 by themselves.** On wrapped faces the bust share rises slowly
   with area (0.572, 0.590, 0.601 at 48, 63, 75 cells, anatomy): the route without a bust costs only 0.004–0.005 per
   cell more than the route with one (about 0.213 against 0.207–0.209), not 0.022 more. At equal area the hull
   starves *more* readily than the wrapped face's own no-bust route (ln τ 13.63 against 14.05 at 63 cells; 10.46
   against 10.78 at 48), and lives longer only because it has no bust route (worth 0.85–0.9). What is specific to
   the rim is the hull's tail price (0.50 per live cell against 0.42–0.44) and a negative rim term (the constant
   b = −0.344 per unit of side that goes with 0.231); neither is derived here.

f. **[measured] Where the 63-cell hull face parts from the 63-cell torus in π(n)** (`hullpi.py`): the hull is
   e^0.9 times as often at 14–16 cells (lower mean, larger variance), e^0.2 at 3–4 cells, e^(−0.26) at one cell, and
   dies from one cell 0.60 times per generation against 0.75: together the 0.47–0.49 of ln τ. Its tail is steeper:
   0.460 per live cell over 4–12 cells against 0.382. That is the only place where the histogram shows the hull's
   higher price; put into the tangent estimate (with all its faults, item 6 below) it raises the price per cell by
   6% where 11% is measured.

g. **[measured] At equal area the tube's bust route is the wide face's; its extra deaths are deaths without a
   bust.** 66 cells, tube (1,5),(0,22) against wide (1,4),(0,22), equal exposure (`pair66.py`; 2,995 and 2,670
   deaths; ln τ 13.657 ± 0.018 and 13.772 ± 0.019): the stationary over-full share is 0.0152 on both; the fall map
   agrees to 0.03 cells at every filling (from 45, 49, 53 of 66 cells: 29.51 / 29.52, 24.11 / 24.14, 17.84 / 17.85);
   the kill g₄(P) agrees within its counts (26/22, 45/48, 66/68, 71/53, 38/41, 15/17 deaths at P = 45 … 55); the
   number of deaths that were over-full four generations earlier is 506 on the tube and 513 on the wide face; and
   the over-full share of dying faces is lower on the tube, 0.169 ± 0.007 against 0.192 ± 0.008 (0.192·e^(−0.115) =
   0.171 if every extra death of the tube were a death without a bust). Also the chance q(n) that a dip to n cells
   ends in death is the same on the 60- and 66-cell tubes and the 63-cell wide face at every n ≤ 20, up to a
   smooth fall with area (q(12) = 0.0104, 0.0092, 0.0104; 0.0136 at 48 cells).

h. **[fitted: one number, the level at which the lead is read] The two-route formula for the tube's discount.**
   If the bust route is the same on tube and wide face (item g) and the route without a bust runs faster on the
   tube by the factor by which the living tube is more often at a given low population,

       D = ln τ_wide − ln τ_tube = ln( b + (1 − b)·e^Δ ),    Δ = ln π_tube(n) − ln π_wide(n) at n = f·P̄, equal area,
       b = bust share of the wide face (anatomy's 0.572, 0.590, 0.601 at 48, 63, 75 cells: logit b = 0.364 + 0.0045 (A − 63)).

   | cells (tube / wide) | Δ at f = 0.525 | b | D from the formula | D measured |
   |---|---|---|---|---|
   | 66: (1,5),(0,22) / (1,4),(0,22) | 0.268 | 0.593 | 0.118 | 0.125 ± 0.007 |
   | 84: (1,12),(0,28) / (1,4),(0,28) | 0.466 | 0.613 | 0.207 | 0.220 ± 0.004 |
   | 96: (1,17),(0,32) / (1,13),(0,32) | 0.661 | 0.625 | 0.301 | 0.302 ± 0.004 (against the wide line; no wide 96-cell lifetime on file) |
   | 108: (1,16),(0,36) / (6,0),(0,6) | 0.848 | 0.638 | 0.394 | 0.381 ± 0.011 |
   | 120: (1,18),(0,40) / (1,11),(0,40) | 0.974 | 0.650 | 0.455 → ln τ = 24.598 | not measured (block M5) |

   Σ z² over the four measured pairs (error floor 0.01): 86.6, 11.4, **3.8**, 24.9, 262 at f = 0.45, 0.50, 0.525,
   0.55, 0.60. So the level is a fitted number, f = 0.52 ± 0.02, about 0.27 A; it is where the falls of item b land
   (0.19–0.36 A), which is what the formula needs (below the landing level the two routes are one stream), but that
   was noticed after the fit. The count-weighted mean of Δ over 0.40–0.55 P̄, the estimator fixed in `pairs.py`
   before the formula existed, gives 0.116, 0.216, 0.310, 0.400 (Σ z² 3.0) but its effective level drifts with the
   sample size; the plateau of Δ near 0.45 P̄ overshoots (0.232, 0.355, 0.465). This is why the tube's lead at half
   population is 2.1–2.25 times its discount: only the 36–41% of deaths that go without a bust profit from it. The
   bending with tube length is the growth of Δ (0.011 per cell from 66 to 84 cells, 0.016 from 84 to 108) on the fat
   lower side of the tube's living fluctuations, set against the falling share of the route that can profit.
   `python3 research/blast/model/tworoute.py` → `data/tworoute_out.txt`. Not checked: that the bust share of a
   wide face follows anatomy's line beyond 75 cells; the equality of the bust route at any size but 66 cells; loop²
   13 and 16.

## Short answer (written before the section above; the front gas has since been killed by agent `anatomy`: no band-first class of deaths)

1. **[fitted] The front gas with one σ fails on the data on file; with a free weight per loop length it fails less,
   and the data prefer growth exponential in the area to a power of the length.** 54 pooled wrapped faces of 48–126
   cells (everything `research/wrap/faces.py` loads, long tubes and the 96-cell faces included):

   | form | parameters | χ² (A ≥ 48, 54 faces) | χ² (A ≥ 36, 58 faces) |
   |---|---:|---:|---:|
   | FG: K·e^(−2σ\|v\|)·L_v^m, every loop direction | 5 (a, c, σ, K, m) | 3160 on 49 | 4473 on 53 |
   | FG2: the same with m = 2 | 4 | 7446 on 50 | 7536 on 54 |
   | SW: K·e^(−2σ\|v\|)·L_v·e^(gA) | 5 | 3350 on 49 | 4453 on 53 |
   | FGq: K_q·L_v^m, K free for loop² 12, 13, 16, 19, 21 | 8 | 358 on 46 (m = 1.70 ± 0.05) | 455 on 50 |
   | SWq: K_q·L_v·e^(g(A−63)) | 8 | 251 on 46 (g = 0.0143) | 322 on 50 |
   | GEN: K_q·L_v^m·e^(g(A−63)) | 9 | 222 on 45 (m = 0.23 ± 0.14, g = 0.025 ± 0.002) | 230 on 49 (m = 0.10 ± 0.10) |
   | HAZ (research/wrap): r_q·e^(g_q(A−63)), rates add | 10 | **87 on 44** | **107 on 48** |
   | EXPA: as HAZ, log-discounts add | 10 | 136 on 44 | 141 on 48 |

   Where FG fails exactly: (a) **the loop-length law is not e^(−2σ|v|).** The share of the death rate per loop
   direction at 63 cells is 0.130, 0.102, 0.055, 0.015, 0.001 ± 0.001 for loop² 12, 13, 16, 19, 21 (HAZ r_q; GEN
   K_21). From 12 to 13 to 16 it falls as e^(−1.3…1.7 per unit of girth); from 16 to 19 as e^(−3.7); from 19 to 21 by
   a factor above 5 for 5% more girth. One σ cannot serve loop² 16, 19 and 21
   together: FG leaves the three equilateral faces 4×4, 57 cells, 63 cells at +20σ, −10σ, −19σ; FG2 at +47σ, −33σ,
   −32σ, and the equilateral faces of 75–108 cells at +10σ to +15σ (it puts a discount on loops of 25–36). (b) **Growth with
   size:** with K_q free, a common power of L leaves the long loop² 12 tubes +6.4σ, +6.8σ (96, 108 cells) and the
   loop² 16 faces −5σ (72, 84, 96 cells); GEN drives m to 0.1–0.2. But no common growth law fits either: g_12 =
   0.0298 ± 0.0005, g_13 = 0.0290 ± 0.0009, g_16 = 0.0226 ± 0.0008 in HAZ. (c) **Small sizes:** refitted with the
   long tubes, HAZ takes the 36- and 39-cell equilateral faces at +2.5σ and +2.1σ (the frozen law of 2026-11-15
   missed them by 16σ and 9σ); FGq and SWq miss them by +4σ to +5σ; FG by −20σ, −10σ. (d) **Rates add better than
   log-discounts** (87 against 136 at equal parameters); the worst multi-loop face is (12, 0, 16) at 48 cells,
   −3.7σ (0.004 in ln τ). What survives of the front gas: D/L² ≈ constant on the loop² 12 tubes is real
   (PI's arithmetic), and the PI's 120-cell number agrees with every form that fits (24.52–24.59).
   `python3 research/blast/model/frontgas.py 48` (and `36`); outputs `data/frontgas_48.txt`, `data/frontgas_36.txt`.

2. **[measured] σ from the empty-patch counts, all shapes: 0.50 to 0.73 per lattice unit, depending on the shape
   family and on the bulk price assumed; no two-term form fits all shapes.** Rhombi from 2×2: σ = 0.55 (c free:
   0.243), 0.71–0.73 (c = 0.2086 forced). Strips 1×b (the shapes nearest to a band): σ = 0.50 (c free: 0.220), 0.52
   (c forced). Every shape of ≥ 12 cells in one fit: σ = 0.42–0.50 with residuals above 1 nat. The strip that wraps
   the 12×12 face (1×12) is 0.45 nats cheaper than the open-strip trend (it has no ends). So "σ ≈ 0.66" is inside
   what the patches allow and is not fixed by them. **[post hoc]** The full cost per unit length of a one-unit-wide
   empty strip, 1.65 (= 3 × 0.55), predicts the ratios of the tube shares between girths as e^(−1.65 Δg): 0.79 and
   0.52 for loop² 12→13 and 13→16, against 0.78 and 0.54 measured (HAZ r_q); it fails beyond (16→19: 0.55 against
   0.27; 19→21: 0.69 against < 0.2). `python3 research/blast/model/patches.py`.

3. **[fitted] The hull faces do not need a second price.** With the wide wrapped price held at c = 0.2086,
   ln τ = c·A + b·k + d + e/k (k the side in unit cells; three free numbers) fits the five hull faces of 30–108 cells
   with χ² 16.8 on 2 (worst 3.1σ = 0.008 in ln τ, at 45 cells); "two prices" (a free price per cell, b·k + d) has
   χ² 152.8 on 2 on the same five (it cannot take the 30-cell face: 10σ) and 0.0 on 1 on 45–108 cells, where
   every three-number form fits (m·ln A: m = −1.45, χ² 0.9; e/k: 2.1). Forecasts: 135 cells 29.17–29.21 (expansion
   forms) against 29.23 (two prices); 165 cells 35.66–35.72 against 35.81. No version of the front gas touches the
   hull's excess: fronts only add ways to die, and a hull face already has the *lower* density and the *larger*
   variance (ρ 0.497, s² 0.436 at 63 cells against 0.517, 0.388 wrapped) yet lives 0.47 longer; its excess is in the
   tail (price per live cell lost 0.50 against 0.42–0.44). `python3 research/blast/model/hull.py`.

4. **[measured] New: the living state of a tube is not the living state of a wide face, and it does not depend on
   the tube's length.** Stationary cumulants per cell of the face population P (1.5 × 10⁸ samples per face):

   | face | ρ | κ₂/A = s² | κ₃/A | κ₄/A |
   |---|---|---|---|---|
   | tube loop² 12, 78 / 84 / 96 / 108 / 120 cells | 0.51542–0.51544 | 0.4024, 0.4021, 0.4022, 0.4023, 0.4023 | −0.491, −0.488, −0.488, −0.489, −0.489 | +2.12, +2.07, +2.04, +2.04, +2.03 |
   | tube loop² 13, 75 / 96 cells | 0.51612, 0.51614 | 0.3972, 0.3967 | −0.465, −0.455 | +2.08, +1.87 |
   | one loop² 16, 96 cells | 0.51699 | 0.3886 | −0.388 | +1.47 |
   | wide (no loop² < 25): 75 / 93 / 108 / 111 cells | 0.51752–0.51773 | 0.3819, 0.3792, 0.3784, 0.3781 | −0.362, −0.319, −0.304, −0.301 | +1.54, +0.98, +0.77, +0.71 |

   (errors: ρ ± 0.00003, s² ± 0.0002, κ₃/A ± 0.004.) A loop² 12 raises the variance per cell by 6% and makes the
   third and fourth cumulants extensive (wide faces' κ₃/A and κ₄/A are still shrinking with area: their non-Gaussian
   part is the tail itself, not extensive). "The differences are not in the living state" (the brief) holds for the
   density to 0.4% and fails for the fluctuations. `python3 research/blast/model/cumulants.py`.

5. **[measured, zero fitted numbers] The tilt estimate from the first two stationary moments gives the size and
   order of the wrapping discounts, not their growth with length.** D_var = A·(λ·δρ + ½λ²·δs²) with δρ, δs² against
   the wide faces at equal area (s²_wide = 0.3703 + 0.858/A) and λ = 0.41 (tail slope of ln π(n), item 6):

   | face | D_var | D measured | ratio |
   |---|---|---|---|
   | loop² 12 tubes, 54 / 60 / 66 / 78 / 84 / 96 / 108 cells | 0.153, 0.158, 0.171, 0.210, 0.229, 0.273, 0.318 | 0.091, 0.117, 0.142, 0.198, 0.224, 0.302, 0.390 | 1.68, 1.35, 1.20, 1.06, 1.02, 0.90, 0.81 |
   | loop² 13, 75 / 96 cells | 0.145, 0.201 | 0.140, 0.236 | 1.04, 0.85 |
   | loop² 16: 4×4 (48 cells), (4,0),(0,8) (96 cells) | 0.154, 0.102 | 0.108, 0.109 | 1.43, 0.94 |
   | loop² 19 ×3 (57 cells); 12 ×3 (36 cells) | 0.057; 0.340 | 0.036; 0.166 | 1.59; 2.05 |

   As a law it fails (Σ z² = 4594 on 20 faces): the tube's moments are constant in its length while its discount
   per cell rises from 0.0017 to 0.0036. **[conjectured]** The rest is in the higher cumulants: the tilt series
   λf + λ²δκ₂/2 − λ³δκ₃/6 + λ⁴δκ₄/24 for the loop² 12 tube reads 0.0009 + 0.0027 + (0.002–0.004) + (0.0015–0.0024)
   per cell and has not converged at fourth order: its sum, 0.007–0.011, is the discount per cell of a long tube
   (measured local value from 96 to 108 cells: 0.0074), i.e. a tube price of 0.198–0.201 per cell. This is the
   PI's front gas seen from the stationary side: a one-dimensional object with its own fluctuation law per unit
   length. `python3 research/blast/model/moments.py 0.41` (output `data/moments_041.txt`).

6. **[measured] The quasi-stationary population distribution π(n) of wrapped faces, down to n = 1** (48, 57, 60,
   63, 66 cells; `data/hist_gen_*.txt`): ln π(n) is Gaussian down to about 0.75 P̄, then bends into a tail whose
   local slope is not constant: it peaks at 0.40 (48 cells), 0.43 (63 cells), 0.44 (66-cell tube) per live cell
   near n ≈ P̄/2 and falls to 0.33–0.39 at 4–8 cells, with an odd–even ripple below 6. The death rate is 0.73–0.78 ×
   π(1). The chance that a dip to n continues to death falls by e^(−0.42…0.45) per cell (63 cells; 0.50 on hull
   faces, `research/dying`). **The tangent construction is not a predictor:** with the slope taken over
   0.15–0.45 P̄, ln τ − [A(λρ − λ²s²/2) + ½ln(2πσ²)] = +0.01, +0.10, −0.25, −0.22, −0.62 at 48, 57, 60, 63, 66
   cells; the window slope rises with area (0.354, 0.367, 0.387, 0.390, 0.411) and ln τ moves by A·x_t ≈ 23 per unit
   of λ. `python3 research/blast/model/qsd.py --summary gen_4_0_4_c1 gen_1_7_19_c1 gen_1_8_20_c1 gen_1_4_21_c1 gen_1_5_22_c1`.

## Ranked models

| # | model, in three lines | fitted numbers | against the anchors | kills it |
|---|---|---:|---|---|
| 0 | **Boom, bust, starve (anatomy's mechanism made quantitative; added last).** 1/τ = Σ_P π(P)·g(P): boom to x ≈ 0.75 A at ψ(x) per cell (measured from the living state, shape-blind), fall to s(x) ≈ 0.36 A (a map of the filling alone), then the survivors starve at the tail price. Hull: no fall, so starvation only. | 0 for the boom; the kill is measured, not derived | boom 0.083–0.098 per cell + kill 0.11–0.15 per cell = 0.21–0.23 (two sizes, peak term only); explains hull > wrapped at equal area (0.47 at 63 cells = no bust route, +0.87, less a readier starvation, −0.4); does NOT give the tube discount (the boom is identical on tubes) nor 0.231 | a wrapped face of 84–108 cells whose dying faces are not over-full at lag 4–5 at ten times the living share; or a tube whose over-full share of deaths equals the wide face's while its lifetime is shorter (then the tube's discount is in the kill) |
| 0b | **Two routes for the tube's discount.** D = ln(b + (1 − b)e^Δ): the bust route is shape-blind (boom, fall, kill and the number of over-full deaths measured equal at 66 cells); the route without a bust is faster on a tube by its stationary lead Δ at the level where falls land. | 1 (the level, f = 0.52 of the mean population); b from anatomy's shares, Δ from living histograms | Σ z² 3.8 on 4 pairs (66, 84, 96, 108 cells): 0.118, 0.207, 0.301, 0.394 against 0.125, 0.220, 0.302, 0.381 | the 120-cell tube outside 24.585 ± 0.06; or a tube of 84+ cells whose number of over-full deaths differs from the wide face's by more than 15% |
| 1 | **Two ways to die, rates add (HAZ refitted).** 1/τ = e^(−a−cA)(1 + Σ_v r_q e^(g_q(A−63))): a short loop opens a second channel at price c − g_q. A description; the only form within reach of the errors. | 10 | χ² 87 on 44 (A ≥ 48), 107 on 48 (A ≥ 36); hull: not addressed | the 120-cell tube above 24.55 (HAZ says 24.51; it is already −2.6σ at 108 cells): then the channel's price is not constant |
| 2 | **A tube has its own price (stationary cumulants).** Tubes are one-dimensional: ρ, κ₂, κ₃, κ₄ per cell independent of length; long-tube price c − Δ, Δ = tilt series of the cumulant differences, 0.007–0.011 for loop² 12. Short tubes cross over. | 0 (λ measured) | second order alone: discounts within 20% at 66–96 cells, ×1.7 at 54, ×0.8 at 108 (Σ z² 4594 on 20) | local slope of the loop² 12 tube from 120 to 240 cells outside 0.196–0.202 |
| 3 | **Rim as an expansion in the side at the wrapped price.** Hull: ln τ = 0.2086·A + b·k + d + e/k. | 3 | χ² 16.8 on 2 (30–108 cells); two prices 152.8 on 2 | the 135-cell hull face at 29.23 or above (expansion: 29.17–29.21) |
| 4 | **Front gas, weight per loop length free (FGq / SWq / GEN).** | 8–9 | χ² 358 / 251 / 222 on 46–45 | already: long tubes +6σ, loop² 16 faces −5σ; and anatomy found no band-first deaths |
| 5 | **Front gas, one σ (FG).** | 5 | χ² 3160 on 49 | dead on file (the cutoff between loop² 19 and 21) |
| 6 | **Tangent construction c = λρ − λ²s²/2 with measured λ.** | 1 (additive constant) | spread 0.63 in ln τ over five faces of 48–66 cells | dead as a predictor; survives as bookkeeping |
| 7 | **Logistic mean field, c = −ln(1 − ρ) − ρ = 0.2116.** No fitted number, 1.4% high. | 0 | wrong tail (slope ln β = 0.73 at n → 0 against 0.35–0.45), wrong s² (0.48 against 0.38), dc/dρ = 1.07 | dead: a coincidence of the integral |

## Forecasts and scores (`PREDICTIONS.md`)

- M1 (commit e0f4d78, before the 96-cell rows were opened): loop² 13 at 96 cells 19.810 ± 0.012, **measured
  19.8109 ± 0.0062 (inside)**; loop² 16 at 96 cells 19.920 ± 0.012, **measured 19.9373 ± 0.0060 (outside, +0.017)
  and 19.9284 ± 0.0063 (inside)**; "the two equal within 0.008": 0.0089 ± 0.0087 (missed narrowly).
  Open: 120-cell tube 24.560 ± 0.020; 240-cell tube 48.0 ± 0.35 (revised in M3 to 48.40 ± 0.25); wide face near 200
  cells: wide line − 0.02 ± 0.06; hull 135 cells 29.200 ± 0.035; hull 165 cells 35.72 ± 0.09.
- M2 (commit 8190fb7, before any 66- or 84-cell histogram was looked at): variance excess of the tube over the wide
  face 0.013 ± 0.005 at 66 cells, **measured 0.0164 (inside)**; 0.021 ± 0.005 at 84 cells, **measured 0.0203
  (inside)**. The reasoning was half wrong (see M3): the excess grows because the wide faces' variance falls.
- Tangent construction "works to 0.3 with one constant": I gave 35%; it fails (spread 0.63).
- M3 (commit e3466c8): the 240-cell tube revised to 48.40 ± 0.25 (local slope 0.1985 ± 0.002 from 120 cells on). Open.
- M4 (commit e46be69, after anatomy's boom and bust): 120-cell tube 24.560 ± 0.020; 240-cell tube 48.40 ± 0.25; wide
  torus of 200 cells 41.716 ± 0.05; hull 135 cells 29.215 ± 0.030; hull 165 cells 35.76 ± 0.08; the inside of a hull
  face busts on its own from side 12 ± 2 (234 cells, range 165–340). All open.
  Its last clause, scored on my 66-cell pair: over-full share of dying faces 0.169 ± 0.007 (tube) against 0.192 ±
  0.008 (wide): "the same within 0.03" holds as written, but the reading is the other branch (the tube's extra deaths
  are deaths without a bust).
- M5 (commit 8f3721c): the two-route formula's number for the 120-cell tube, 24.585 ± 0.030; my own number moved
  to 24.575 ± 0.025. Open.
- The times in the block headers run two to five minutes ahead of the machine clock; the commits carry the true order.

## What was run, and on what it rests

- Stepper: `research/dying/ex3.c` (512 bit-sliced replicas on a cell graph from `research/theory/symmetric/geom.py`;
  renewal lives from 0.4 soups; P histogram over exposure at age > 512; excursion table by minimum P).
- **Validation (mine):** `python3 research/blast/model/validate.py 1500` → `data/validate_out.txt`, ALL OK: for each
  of 8 wrapped slabs (48–84 cells) and 3 hulls (45–84 cells), `sy trace` on the graph file equals a naive stepper
  written from `reference/oracle.py`'s offsets and rule constants (populations at every generation 0–1500, cell sets
  at generations 1, 2, 3, 10, 100, 1500); one redirected neighbour slot fails; ex3's lives file is byte-identical to
  sy's. Not validated this way: the faces used only for stationary moments beyond that list (96–120 cells and
  others: same code path, graphs from the same generator), and ex3's histogram bookkeeping (cross-checks: my ln τ
  from the same files agree with the anchors: 9.931 ± 0.005 / 9.9251, 11.874 ± 0.007 / 11.8751, 12.422 ± 0.008 /
  12.423, 13.152 ± 0.009 / 13.1622, 13.668 ± 0.012 / 13.646).
- Runs: `queue1.sh` (long histograms; killed after the 66-cell tube to save time), `queue2.sh` (short runs for the
  moments, 150,000 generations × 512 replicas each; the long 84-cell pair was abandoned) and `queue3.sh` in scratch
  (ex5: `ex5.c` = ex3.c plus the population 1–15 generations before each death and the joint histogram of
  consecutive populations; its lives file is byte-identical to sy's on the 4×4 torus; outputs `data/hist5_*.txt`). ex3 counts faces of at most 127 cells,
  so nothing above 120 cells.

## Failed, in a line each

- min over x of [ψ(x) + λ·s(x)] as a formula for the bust route's price: 0.275 at 48 cells against 0.207.
- The population chain with the measured one-step kernel as a model of τ: it reproduces ln τ to 0.001–0.017, but it
  must (the stationary marginal is a left eigenvector of the empirical kernel); an identity, not a test.
- Tangent construction as a formula for c or for the discounts: too sensitive to λ, and λ is not a constant.
- "The growth of the tube discount with length is a growth of its variance" (M2's reasoning): the tube's variance is flat.
- A single exponential in the girth for the loop weights (the patch strip cost): right from 12 to 16, wrong beyond.
- A Poisson gas of identical band voids as the whole of (f, δκ₂, δκ₃, δκ₄): the sizes it implies disagree
  (δκ₂/f = 15 live cells, δκ₃/δκ₂ and δκ₄/δκ₃ = 4–10).

## Not checked

- No derivation of λ from the rule (the brief's line 1): not attempted in the time.
- The long 84-cell pair was abandoned; `pairs.py` uses the short runs there (down to 0.25–0.4 P̄ only).
- The bust share per death (the largest fall of each death) was not measured here: `boom.py` works from marginals at
  fixed lags, and the "8 times as deadly" and the split of item d lean on anatomy's table.
- ex5's two added tables were checked only by the identities they must satisfy (Σ_P DL[L][P] = deaths at every lag;
  the J table reproduces ln τ to 0.001–0.017).
- Hull histograms (ρ, s², tail) were taken from `research/dying/README.md`, not rerun.
- Errors of the hull fits use the tabulated statistical errors only; the 30-cell face may carry small-size effects
  that no expansion should be asked to fit.
- The wide reference for s² rests on four faces (75–111 cells); λ = 0.41 is a round value between the measured
  0.39 and 0.44; the ratio column moves by about ±8% for ±0.02 in λ.
- Sweep or flash (the brief's line 4) was not confronted beyond what GEN says (growth exponential in A, i.e. a
  second price, is preferred to a count of places).
- Other agents' directories were not read.
