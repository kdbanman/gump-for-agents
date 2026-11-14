# The thinnest face (interim; work in progress, 2026-11-14)

*Interim note, written while runs are in flight so that nothing is lost if the session ends. The final write-up
replaces it. Numbers below are from `python3 analyze.py life 'det_*'` etc. on the chunk files in
`research/scratch/thin/`; curated copies in `data/` (`python3 collect.py`). Forecasts and scores: `PREDICTIONS.md`.*

## Object

Gump (B45/S345 on the faces of the cubic honeycomb) on the twisted torus with in-plane periods (1,1), (0,b): the
class "shortest loop squared 3" of `research/shape2`. Every cube of a {111} layer has a unique representative
(0, c, t − c): a layer is a **ring of b sites, three cells each** (X_c, Y_c, Z_c), A = 3b. `thin.py table` derives
the 12 neighbours of each orientation as (layer shift, orientation, site shift) from the offsets of
`docs/AUTOMATON.md`; site shifts are at most 2. Along the axis the cells are ordered … Z_c, {Y_c, X_{c+1}},
Z_{c+1}, …: a face is a chain alternating one cell and a pair. "Site s" in window statistics means
{Z_s, Y_s, X_{s+1}} (contiguous).

## Tools and validation

- `thin.py`: geometry, reference stepper (numpy). `python3 thin.py oracle 16 8 300`: equal to
  `reference/oracle.py` on the cubic 16-torus, every cell of every copy, 300 generations.
- `ring.c` (+ `run.py`): rings packed in 64-bit words, 8 rings per AVX-512 vector; deterministic slab (m = 8, two
  faces) or the rule on w layers over two layers of coins; optional wall (face cells of G sites held dead).
  `python3 run.py validate` → ALL OK: every lane-step of dumped runs equals the reference stepper (deterministic,
  model, with and without wall; life ends and exposure recounted), coin statistics, and populations equal to the
  engine on the cubic torus for 3,000 generations (b = 24).
- `exact1.py`, `sweep.py` + `sweep.c`: the one-layer model solved exactly (two independent implementations:
  einsum over translation orbits; triple-by-triple sweep). Ring b = 5: ln τ = 3.967199 from both;
  `ring.c` simulation of the same model: 3.96708 ± 0.00069 (2.1 × 10⁶ deaths, T0 = 40).

## Measured so far (ln τ per face; T0 = 256)

| b | A | deterministic ring | local slope per cell |
|---|---|---|---|
| 16 | 48 | 8.6470 ± 0.0016 | |
| 20 | 60 | 10.0199 ± 0.0036 | 0.1144 |
| 24 | 72 | 11.3447 ± 0.0063 | 0.1104 |
| 28 | 84 | 12.648 ± 0.008 | 0.1086 |
| 32 | 96 | 13.923 ± 0.014 | 0.1063 |

(Census: 8.6426(20), 10.0201(29), 11.3481(40).) The slope is still falling at A = 96.

Rule on w layers over coins (density 102/256), model − deterministic ring: b = 16: +1.286, +1.382, +0.495,
+0.049, +0.006, +0.012 for w = 1…6 (errors 0.003–0.004); b = 24: +1.87, +2.26, +0.85, +0.115, −0.012 ± 0.022
for w = 1…5. **Noise is enough on the thin torus from five layers**; shallower models are much too tough.

Looking back from a death the face population falls linearly in time, and the lag at which half of it is gone
grows linearly with b (4.2, 5.4, 6.6, 7.8, 8.9 generations at b = 16…32): the thin face dies by an island that
shrinks from both ends at about 0.85 sites per generation per end, not in a flash.

## Not checked

Everything not listed above.
