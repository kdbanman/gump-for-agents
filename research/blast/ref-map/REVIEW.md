# REVIEW (ref-map) of "the two prices are two minimum actions of one measured map" — PRELIMINARY, 04:58 UTC

Own stepper (`gs.c`, identical to the oracle for 1,100 generations on hull 9, 11, 13 and the 63-cell torus, negative
controls fail: `validate.out`), own tallies, own dynamic programming (`dp.py`). `ref-anatomy`'s code was not read or run.

Results so far [computed from my measured maps; B = the whole layer beneath the face inside the hull, which has
exactly A cells; rule: cells with n ≥ 200]:

| hull face | gump ln τ (mine) | minimum action S | S/A | chain's exact ln τ |
|---|---|---|---|---|
| 45 cells | 9.818 ± 0.002 | 10.182 ± 0.007 | 0.2263 | 10.19–10.28 |
| 63 cells | 13.659 ± 0.010 | 14.640 ± 0.032 | 0.2324 | 14.22–14.47 |

- S(63) reproduces (`ref-anatomy`: 14.572), and so does the 13-generation fade.
- But S/A is not a price: between 45 and 63 cells S rises by **0.2477 per cell**, gump's ln τ by 0.2119. The chain cannot
  have both gump's slope 0.231 and gump's negative term in k: the pair (0.231, −0.34) requires a first difference of 0.212.
- With B = only the part of the layer beneath that lies under the face (30, 45 cells) the cheapest route is NOT a fade:
  it is a jump and a crash, (34,20) → (40,29) → (22,6) at 63 cells, S = 13.84.
(84 cells and the torus: running.)
