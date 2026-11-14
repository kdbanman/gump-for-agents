# Forecasts (thin line), committed before the runs that test them

Append-only. Each block says what was known when it was written. Scores are added below each forecast after the
run, misses included. Sizes: b = sites round the ring of the torus (1,1),(0,b); face area A = 3b cells.
ln tau is per face (hazard among living lives older than T0 = 256).

## Block 1 (2026-11-14, before any lifetime run of this line)

Known: the census values ln tau = 8.6426(20), 10.0201(29), 11.3481(40) at b = 16, 20, 24 (research/shape2);
`ring.c` validated cell by cell against the reference stepper and the oracle (`run.py validate`), a timing run,
and one 3,000-generation dump at b = 24 used only for the density by layer (0.444 face, 0.397 layers 2-5).
No lifetime or model number of this line has been looked at.

**F1 (reproduction).** `ring.c` (deterministic, m = 8) gives ln tau within 3 sigma (errors combined) of the
census at b = 16, 20, 24.

**F2 (the slope keeps falling).** The two census increments are 1.3775 (b 16 -> 20) and 1.3280 (20 -> 24). Two
forms fitted exactly through the three points: ln tau = a + g b + c ln b gives g = 0.2767 per site, c = 1.213;
ln tau = a + g b + c / b gives g = 0.3073, c = -11.9. Forecast: the deterministic values lie between the two
forms, widened by 0.02:

| b | A | log form | 1/b form | forecast interval | "slope stays 0.333 per site" (alternative, forecast to fail from b = 32) |
|---|---|---|---|---|---|
| 28 | 84 | 12.642 | 12.648 | 12.62 - 12.67 | 12.680 |
| 32 | 96 | 13.911 | 13.930 | 13.89 - 13.95 | 14.012 |
| 36 | 108 | 15.160 | 15.200 | 15.14 - 15.22 | 15.344 |
| 40 | 120 | 16.395 | 16.462 | 16.37 - 16.48 | 16.676 |
| 48 | 144 | 18.83 | 18.97 | 18.81 - 18.99 | 19.34 |

Cost per cell between b = 40 and 48: 0.1015 - 0.1045 (it was 0.1148 at 16 -> 20 and 0.1107 at 20 -> 24).
Asymptotic cost per cell (a guess, not a fit): 0.097 +- 0.008.

**F3 (is noise enough on the thin torus).** Model = the rule on the top w layers over two layers of coins of
density 102/256, one face. Forecast for (model - deterministic) in ln tau, at b = 16 and b = 24, by analogy
with the wide faces (exponent.md section 5):

| w | forecast |
|---|---|
| 1 | between -1.5 and -0.3 (too weak) |
| 2 | between +0.3 and +1.2 (too tough) |
| 3 | between +0.05 and +0.30 |
| 4 | within +-0.08 |
| 5, 6 | within +-0.03 |

**F4 (the coin density hardly matters at depth).** w = 5, b = 20: coin densities 0.30 and 0.55 give ln tau
within 0.05 of the value at 0.398.

**F5 (static formulation).** E(l) = probability that l given consecutive sites of the face are empty
(site s = {Z_s, Y_s, X_{s+1}}, three cells contiguous along the axis), measured on a living deterministic ring
of b = 64; k(l) = -ln[E(l+1)/E(l)].
(a) k(l) decreases with l, and its mean over l = 30..40 is within 0.02 of the lifetime slope per site between
b = 32 and b = 48.
(b) ln tau(b) + ln E(b - s) is constant within +-0.10 over b = 16..48 for one shift s between 0 and 6 sites.
