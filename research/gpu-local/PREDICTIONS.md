# research/gpu-local: forecasts committed before the results

Append-only: corrections go in new dated blocks. Header times from `date -u`.

## 1. The guard on the queued runs, and the hull face at A = 108 (2026-11-15T04:18Z, HEAD 8d465b2)

Written before any measurement run on this card (only checks, guard tests and a throughput benchmark have run). The
forecasts for the equilateral tori are the lead's, in `research/constant/PREDICTIONS.md` part C and its addendum; I add
none of my own for ln τ there, only for what the guard will see.

**Kind-5 lives (cycles the kernel does not recognise, period > 128).**
- Equilateral tori, A = 81 to 111, 8 layers: detected settling of any kind was 0 in every slab run of A ≥ 90 on file
  and falls steeply with size below that (`research/gpu/README.md` "Zombie lives"). Forecast: **no kind-5 life** in
  the A = 93 run (3 × 10⁴ face deaths), probability 80%; if any appear, fewer than 5, carrying < 10⁻⁴ of the
  exposure. Same for A = 108 and 111. At A = 81 and 84 (10⁵ deaths each): 0 to 3 kind-5 lives, 70% on zero.
- Hull octahedron R = 15 (A = 108), 10⁴ deaths: no kind-5 life, probability 85%. The alternative I cannot exclude
  from the data on file: the earlier run (1,059 deaths, under one mean life long) has no age bound on zombies at all.

**ln τ_face of the asymmetric hull face at A = 108** (R = 15, soup 0.35, T0 = 200, τ_face = 8 × exposure / deaths,
guard on with thresholds 16 · 2^j). On file: 23.376 ± 0.031 (1,059 deaths, one run). A smoothness reading of the
local slopes (0.2119, 0.2146 for 45→63→84, then 0.2181 ± 0.0013) puts the slope 84→108 at 0.2173 to 0.2181, that is
ln τ at 23.36 to 23.38.
- Forecast: **23.37 ± 0.03** for the new run on its own (planned statistical error ± 0.010). I expect the new value
  inside 23.31 to 23.44 with 95%.
- If it lands below 23.31: the old run was a high draw or carried unrecognised cycles (then kind-5 lives should be
  seen here, see above). Above 23.44: a high draw now, or the hazard is not flat at ages the old run did not reach
  (it reached ≤ 6 × 10⁸; this run will pass 10¹⁰): check the hazard by age before believing either.
- Probability that the new value is lower than the old by more than 0.031: 20%.
