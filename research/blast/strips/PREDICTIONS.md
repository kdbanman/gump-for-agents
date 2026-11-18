# blast/strips: forecasts, frozen before the data (agent `strips`, 2026-11-18, second phase)

## Block A. Frozen 12:45 UTC, before any strip, tube or tetrahedron lifetime was computed by this agent

Seen before writing (so not forecast): `rim/README.md` (its table of symmetric strips, 8 to 14 half-rows, L = 3…6),
`holes/README.md` and `holes/data/life_tori.txt` (closed tori 2…4 × 3…8, all first deaths), the lead's
`research/constant/out/points.txt` (closed rectangles 3×6, 3×8, 3×10, 4×4…4×9, 5×5…5×8, 6×6, 6×7, firewall
channel resolved), the anchors in `BRIEF-COMMON.md`. Not seen: the PI's block 6, anything under `noisy/`, any
tetrahedron lifetime, any strip with L = 7 or (5 unit rows, L = 6).

Notation: strip (w, L) = prism |x+y| + |z| ≤ R = 2w − 1 with period L·(2,−2,0); w unit rows (rim's 2w rows),
3wL cells per face. Probabilities are mine; "±" is my 68% band.

A1. **Referee's part.** My code, my conventions (soup 1/2, T0 ≥ 200, period ≤ 12 censored) reproduces all nine of
rim's values (8,8,3…6), (10,10,3…5), (12,12,3), (12,12,4) within 3 combined standard errors: **P = 0.70**.
(If it fails, I expect the failure at L = 3, the shortest-lived, from the convention and not from the stepper.)

A2. **(4 unit rows, L = 7).** ln τ = **18.97 ± 0.10**. Length price at L 6→7 (per cell, 12 cells):
**0.208 ± 0.008**. P(price < 0.2127, i.e. nearer 0.209 than 0.217, or below both) = **0.60**; P(≥ 0.2127) = 0.40;
P(< 0.200, the rod beginning to die as a rod) = 0.20. I expect the fall to continue, slower (steps so far
−0.0147, −0.0131).

A3. **(5 unit rows, L = 6).** ln τ = **20.15 ± 0.12**. Width price at L = 6 (per cell, 18 cells, 4→5 unit rows):
**0.2045 ± 0.006**; P(it exceeds 0.2017, i.e. goes on rising) = 0.65; P(it exceeds 0.2087) = 0.2. Mixed second
difference at (4.5 rows, L 5→6): **0.218 ± 0.03** (P(< 0.2262, the value one step earlier) = 0.6).

A4. **Do the two prices meet?** [conjecture] They cross between L = 6 and L = 8, at **0.205 ± 0.007**, i.e. at or
slightly below the wrapped 0.209, not at 0.22–0.23: P(crossing value < 0.2127) = 0.65. After crossing I expect
the length price to go on falling slowly (a strip of fixed width is a one-dimensional object at large L).

A5. **Firewalls in strips** (three consecutive dead layers of a diagonal that is not a face's, which cut the
prism across its axis). Share of first face deaths preceded by one: (4 rows, L = 4) < 2% (P = 0.8);
(4 rows, L = 6) < 10% (P = 0.6); (3 unit rows = rim's 6×6 rod, L = 6) > 50% (P = 0.7).

A6. **Closed tubes with my code** (controls; I have seen the lead's values): my 4×4, 4×5, 4×6, 5×5 agree with
9.9324, 12.4865, 14.9710, 15.6614 within 0.02 when booked the lead's way: P = 0.8. Unseen: 3×4, 3×5, 3×7 booked
without firewall-preceded deaths: 7.39 ± 0.03, 9.27 ± 0.05, 12.85 ± 0.15. The row of a rimmed strip is cheaper
than the row of a closed tube of the same girth by 0.020, 0.011, 0.006 per cell at L = 3, 4, 5 (this is
arithmetic on tables I have seen, not a forecast).

A7. **Tetrahedron** (four alternate half-spaces, side s, faces of 3s(s+1)/2 cells, all rims sharp). Guess:
shorter-lived than the octahedron's faces of equal area, because a sharp rim row is cheap and the body is thin:
ln τ_face = **4.0 ± 0.6 (s = 3; may have no steady hazard), 5.9 ± 0.8 (s = 4), 8.6 ± 1.0 (s = 5), 12.0 ± 1.2
(s = 6), 16.0 ± 1.5 (s = 7)**. P(below the octahedron at every side 4…6) = 0.75. Second differences per cell:
0.30 ± 0.06 (s = 4), 0.25 ± 0.04 (s = 5), 0.235 ± 0.03 (s = 6). P(the s = 6 second difference lies within 0.015
of the octahedron's 0.2313) = 0.45.

A8. **How they die.** Tetrahedron faces fade: share of deaths with a one-generation fall of at least half the
face < 0.05 (P = 0.6). Strips: I have seen rim's 0.15–0.20.

Record so far on this problem (others'): about 40% held. Expect the same of these.
