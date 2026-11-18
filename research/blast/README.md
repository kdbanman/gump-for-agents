# research/blast: why does a face die at the rate it does? (the night of 2026-11-18)

Standing account of the PI (the session in charge of the blast). One subdirectory per agent, each with its own
README; `BRIEF-COMMON.md` is what every agent was told; `PREDICTIONS.md` holds forecasts frozen before data;
`REPORT.md` is the account for the owner. Written to as results are checked; newest state at the top.

## State (03:20 UTC)

Wave 1 launching: eight Fable agents, one angle each.

## The front gas (the PI's reading at 03:31 UTC; conjecture; forecasts in PREDICTIONS.md block 1)

Arithmetic on anchors already on file (BRIEF-COMMON.md and `research/gpu-local/README.md`, chain 3):

    python3 -c "
    import math
    w=lambda a:13.1623+0.20861*(a-63)
    for a,v in ((54,11.1935),(60,12.4219),(72,14.8755),(84,17.3175),(96,19.7446),(108,22.1599)):
        D=w(a)-v; L=a/12; print(a, round(D,3), round(D/L**2,5), round(math.exp(D)-1,3))"

gives D/L² = 0.0045 … 0.0048 for tubes of loop² 12 over a factor two in length: the tube discount is quadratic in
length, and its coefficient falls with girth as e^(−2σg), σ ≈ 0.66 per lattice unit, the edge cost of an empty
patch. Reading: two-stage deaths through a band right round the girth; a gas of fronts.

### The PI's own check of the front-gas form on the faces on file (03:45 UTC) [fitted; one code; loader of research/wrap]

`python3 research/blast/pi/frontgas_check.py 64 48` (10 s; 54 pooled wrapped faces of 48 cells and up; errors floored
at 0.0015).

- **Single short loop: a rate share ∝ L^m with one m for every girth fits.** On the 45 faces with at most one loop²
  ≤ 19: ln τ = a + c(A − 63) − ln(1 + ε_q·L^m), L = area/girth, gives χ² 60.7 on 34 with m = 2.32, c = 0.20878,
  ε = e^(−5.87), e^(−6.06), e^(−6.51), e^(−7.64) at loop² 12, 13, 16, 19 and **nothing at 21 and beyond** (the free
  strengths go to zero). So the growth with length is common to all girths, and the lead's "the discount ends
  between 19 and 21" survives in this form: ε_q ≈ 0.00033·(20.5 − q), linear in loop², not e^(−2σg) (the three
  girths 12, 13, 16 alone give σ = 0.58–0.60; the step to 19 is three times steeper). **My block-1 item 4 (wide
  tori carry the same term through loops of 21–36) is not supported by the data on file.**
- **Several short loops: rates do not simply add.** All 54 faces with one term per loop direction: χ² 200 on 43 and
  m drops to 1.6; the 4 × 4 (three loops of 16) and the long 12-tubes pull opposite ways. With ε_q = K e^(−2σg)
  imposed for every loop: χ² 971 on 49. So the form is a description of tubes, not yet a law of all wrapped faces.
- An exponential share with a site factor, r = B·L·e^(gL) with g = 0.19–0.20 per lattice unit (0.016 per cell),
  fits the loop-12 family as well as the power: the measured d ln r/d ln L is 2.26, 2.12, 2.30, 2.48, 2.56 at
  L = 4.75 … 8.5, and 1 + 0.195·L is 1.93, 2.07, 2.27, 2.46, 2.66. The two readings (bands with an entropy ∝ L^m;
  a collapse that spreads at a lower price per cell after starting somewhere) part at 200+ cells: slope returning
  towards a girth price near 0.198–0.201, against levelling at 0.192.
- Not checked: no second code; the choice of error floor; faces below 48 cells.
