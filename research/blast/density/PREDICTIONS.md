# Forecasts of research/blast/density, second task (frozen 13:58 UTC 2026-11-24, before any of its runs)

Written by the solver before any row of this task has run, and before reading block 5 of
`research/blast/noisy/PREDICTIONS.md`. Known when written: everything in `README.md` up to commit 9a105d3 (at 63 cells,
ε = 1/4, d = 1, coins of density p at every replaced depth: −0.32, +0.04, +0.27, +0.43, +0.68, +0.98 at p = 0.1 … 0.7,
zero near 0.19; at ε = 1/16 the mean-density coins give +0.164 against +0.532 at 1/4, i.e. about in proportion to the
replacement probability 0.061 against 0.221). Nothing at ε = 1 (full replacement), nothing at 45 cells with coins.

"Full replacement" (the PI's ε = 1): every replaced cell is a fresh coin every generation. p\*(ε, A) = the coin density
at which the watched face's ln τ equals gump's, from interpolating Δ ln τ against p.

My reading [conjectured]: for small ε the effect is linear in the replacement probability q at fixed p (Δ ≈ q h(p)),
so p\* does not move between ε = 1/16 and 1/4. At full replacement there are no rule-made cells left in the core,
and part of what a coin does at ε = 1/4 is to hold up the rule-made cells around it; I expect that to shift p\*, and
I do not know the direction well; I lean to higher (an independent support has to be denser to replace gump's when
it no longer props up gump-made neighbours). The size: the 45-cell face has 3 replaced cells under it in layer 1 (63
cells: 9), so its gains are smaller, and the zero is less sharply located.

1. p\*(ε = 1/16, 63 cells) lies within 0.05 of p\*(1/4, 63): **65%**.
2. p\*(1/4, 63) refined lies in [0.17, 0.21]: **75%**.
3. p\*(full, 63) lies within 0.05 of p\*(1/4, 63): **40%**. It is higher than p\*(1/4, 63): **60%**.
4. The slope dΔ/dp at p\* is larger at full replacement than at 1/4 (at least 1.5 times): **70%**.
5. p\*(1/4, 45 cells) lies within 0.05 of p\*(1/4, 63): **50%**.
6. At full replacement, coins of the 63-cell p\* give the 45-cell face gump's life within ± 0.03 in ln τ: **40%**
   (that is, one density serves both sizes).
7. At full replacement and p ≈ p\*(full, 63): the share of descents to ≤ 1 cell that die is gump's 0.77 within ± 0.03:
   **75%**; and every Δ ln f_k and Δ ln P_k (k = 1 … 15) is within ± 0.06 of zero: **45%** (the way of dying the
   same as gump's, not only its rate).
8. At ε = 1/4, p = 0.8: Δ ln τ > 0: **97%**; in [1.0, 1.5]: **60%**.

## Third task (frozen 15:07 UTC 2026-11-24, before any of its runs, before reading block 6 of `research/blast/noisy/PREDICTIONS.md`)

Known when written: everything in `README.md` up to b7f5904. On coins alone (full replacement, DO = 1) p\* = 0.3848
(45 cells) and 0.3854 (63 cells); one 84-cell row at 0.385 reads −0.28 ± 0.15. Gump's replaced *core* of layer 1 at
63 cells (9 cells) has density 0.430 overall and 0.384 when the face has ≤ 10 cells; the whole layer 1 (63 cells)
0.441 and 0.342. Not known: the density of the cells DO = 1 actually replaces (45 of layer 1's 63 at 63 cells, 30 of
45 at 45 cells), nor anything at 45 cells.

My reading [conjectured]: the coincidence is an accident of comparing the core (9 cells) with coins that fill 45 cells
of layer 1 and everything below. The set DO = 1 replaces includes cells nearer the rims, which fade more than the core
under a low face, so its thinnest density will be below 0.38 at 63 cells. Skin depth: a face's rate depends mostly on
its first two layers (part 1: d = 2 → 1 adds +0.35, d = 6 adds nothing), so fresh coins at gump's own mean densities
from depth 3 or 4 on should give nearly gump's rate; the way of dying needs the face's real support, and I expect it
to converge more slowly than the rate.

1. At 63 cells, the density in gump of the 45 cells of layer 1 that DO = 1 replaces, at its minimum over face ≤ 2, 4,
   6, 10, 15, 20, is within 0.01 of 0.385: **25%**. At 45 cells (the 30 cells of layer 1 DO = 1 replaces): **30%**.
   The coincidence survives at both sizes (both within 0.01): **12%**.
2. Skin depth, full replacement at each replaced cell's own layer mean density in gump (column A: depth ≥ d under the
   watched face, ≥ 3 under the others; column B: depth ≥ d under every face):
   a. A, d = 1, 63 cells: Δ > +0.5: **85%**. B, d = 1, 63 cells: Δ > +2: **75%**.
   b. A, d = 3, 63 cells: |Δ| < 0.10: **55%**. A, d = 4: |Δ| < 0.05: **60%**.
   c. B, d = 3, 63 cells: |Δ| < 0.10: **35%**. B, d = 4: |Δ| < 0.10: **50%**.
   d. Δ falls monotonically with d in both columns at both sizes: **70%**.
   e. In the first row of each column (63 cells) with |Δ| < 0.05, death from one cell is gump's 0.77 within ± 0.03
      and Δ ln f_15, Δ ln P_15 are within ± 0.10: **35%** ("a skin of d layers gives the rate and the way").
   f. The way of dying (P_1) converges to gump's more slowly in d than the rate does: **65%**.
3. 84 cells, coins alone at p = 0.385, all chunks pooled: |Δ| < 0.10: **40%**; Δ < −0.10: **45%** (p\* creeps up).
