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
