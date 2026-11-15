# The wrapping law: forecasts written before any new face is measured

The lead, 2026-11-15 13:02 UTC. The law and how it was found are in `research/NOTEBOOK.md` (entry "the kink is the
wrapping") and `research/audit/wrap_law_lead.py`. In one line: a wrapped face of A cells whose closed loops all have
squared length ≥ 12 lives

    ln τ_face = 13.1629 + 0.20860·(A − 63) − (A − 21.25) · Σ over loop directions v of k(|v|²),
    k(12) = 0.002918, k(13) = 0.002271, k(16) = 0.001353, k(19) = 0.000338, k(q ≥ 21) = 0,

one direction per ±v. These seven numbers are frozen (`wrap_law_lead.py`, `FROZEN`); the forecast for any torus is
`python3 research/audit/wrap_law_lead.py --predict H K D`. They were fitted to 32 faces (χ² 42.0 on 25), so the fit
itself is not a test. What would be:

- **W1 (65%).** New faces: every class with shortest loop² ≥ 12 at areas not in the fit (A = 51 to 69 on the CPU),
  measured to ± 0.005 or better, lands within 0.010 of its frozen forecast, or within 3 standard errors if that is
  wider. One class outside by more than twice that margin and the law, as an additive law, is refuted.
- **W2 (70%).** New faces with every loop² ≥ 21 (no discount) land within 0.006, or 3 standard errors, of the line
  13.1629 + 0.20860·(A − 63).
- **W3 (65%).** With the new faces in, a free k(21) stays below 0.00008 (a quarter of k(19)): the discount ends
  between loop² 19 and 21 and does not tail off.
- **W4 (40%).** Additivity holds for pairs of short loops at new areas to the same accuracy as for single ones: the
  residuals of faces with two or more short directions are no larger than those with one.
- **W5 (35%).** The law extends below its range with one more number each: adding k(9) (and k(7)) with the same A0
  describes the classes of shortest loop² 9 (and 7) at χ² per degree of freedom below 2, including the sign changes
  of SH7.
- **W6 (50%).** The pairs already on file that the law gets wrong keep getting it wrong when re-measured: the two
  loop² 12 classes at A = 60 (law: equal; measured 0.0069 ± 0.0024 apart) still differ by more than 0.004. If so
  there is a second, smaller effect of loops longer than 20 at small areas.

What I expect to be wrong about: the form (A − A0). Fitted on faces of 60 cells and more it gives A0 = 27 and
puts all four 48-cell faces 0.003 to 0.013 too high, so the discount is probably not exactly linear in area.
